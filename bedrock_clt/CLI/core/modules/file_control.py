import os
import shutil
from pathlib import Path

from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style


STYLE = Style.from_dict({
    "frame":            "#2d3748",
    "frame.top":        "bg:#0d1117 #f0a500 bold",
    "frame.bottom":     "bg:#0d1117 #3d4f61",

    # ── Header / breadcrumb ─────────────────────────────────────────────────
    "bc.root":          "bg:#0d1117 #4a90d9",
    "bc.sep":           "bg:#0d1117 #2d3748",
    "bc.part":          "bg:#0d1117 #8ab4c9",
    "bc.current":       "bg:#0d1117 #e2e8f0 bold",

    # ── Lista – item normal ─────────────────────────────────────────────────
    "item.pre":         "bg:#0d1117 #2d3748",   
    "item.icon":        "bg:#0d1117 #4a90d9",   
    "item.name":        "bg:#0d1117 #8ab4c9",    
    "item.pad":         "bg:#0d1117 #0d1117",  

    # ── Lista – item seleccionado ───────────────────────────────────────────
    "sel.pre":          "bg:#1a2535 #f0a500 bold",
    "sel.icon":         "bg:#1a2535 #f0a500",
    "sel.name":         "bg:#1a2535 #ffffff bold",
    "sel.pad":          "bg:#1a2535 #1a2535",

    # ── Lista – item denegado ───────────────────────────────────────────────
    "deny.icon":        "bg:#0d1117 #3d4f61",
    "deny.name":        "bg:#0d1117 #3d4f61 italic",

    # ── Scrollbar ───────────────────────────────────────────────────────────
    "scroll.track":     "bg:#0d1117 #1e2d3d",
    "scroll.thumb":     "bg:#0d1117 #f0a500",

    # ── Footer ──────────────────────────────────────────────────────────────
    "ft.key":           "bg:#0d1117 #f0a500 bold",
    "ft.label":         "bg:#0d1117 #4a6070",
    "ft.sep":           "bg:#0d1117 #1e2d3d",
    "ft.count":         "bg:#0d1117 #2d6a4f bold",
    "ft.countval":      "bg:#0d1117 #52b788 bold",
})



def _tsize() -> tuple[int, int]:
    s = shutil.get_terminal_size(fallback=(80, 24))
    return s.columns, s.lines

def _max_visible(rows: int) -> int:
    return max(3, rows - 4)



#  Filesystem
# ─────────────────────────────────────────────────────────────────────────────
def _listar(ruta: Path) -> list:
    items = []
    try:
        for e in sorted(ruta.iterdir(), key=lambda p: p.name.lower()):
            if e.is_dir():
                ok = os.access(e, os.R_OK | os.X_OK)
                items.append((e, ok))
    except PermissionError:
        pass
    return sorted(items, key=lambda t: (not t[1], t[0].name.lower()))


#  Scrollbar ASCII
# ─────────────────────────────────────────────────────────────────────────────
def _scrollbar(total: int, offset: int, visible: int) -> list[str]:
    if total <= visible:
        return ["░"] * visible
    thumb_size = max(1, round(visible * visible / total))
    thumb_pos  = round(offset * (visible - thumb_size) / (total - visible))
    bar = []
    for i in range(visible):
        if thumb_pos <= i < thumb_pos + thumb_size:
            bar.append("█")
        else:
            bar.append("░")
    return bar


#  Breadcrumb
# ─────────────────────────────────────────────────────────────────────────────
def _breadcrumb(ruta: Path, cols: int) -> list:
    partes = list(ruta.parts)   
    tokens = []

    full = []
    for i, p in enumerate(partes):
        es_raiz = (p == "/")
        es_ultimo = (i == len(partes) - 1)
        label = " " if es_raiz else p
        if es_ultimo:
            full += [("class:bc.current", f" {label} ")]
        else:
            full += [
                ("class:bc.part" if not es_raiz else "class:bc.root",
                 f" {label} "),
                ("class:bc.sep", "❯"),
            ]

    # Si es demasiado largo, colapsar con …
    raw_len = sum(len(t[1]) for t in full)
    if raw_len > cols - 6:
        # Solo mostrar los 2 últimos niveles
        short = partes[-2:] if len(partes) >= 2 else partes
        tokens = [("class:bc.sep", " … ❯")]
        for i, p in enumerate(short):
            es_ultimo = (i == len(short) - 1)
            if es_ultimo:
                tokens += [("class:bc.current", f" {p} ")]
            else:
                tokens += [
                    ("class:bc.part", f" {p} "),
                    ("class:bc.sep",  "❯"),
                ]
    else:
        tokens = full

    return tokens

# ─────────────────────────────────────────────────────────────────────────────
#  Renderizadores de secciones
# ─────────────────────────────────────────────────────────────────────────────
def _render_top(ruta: Path, cols: int) -> list:
    title = " BEDROCK-CLT  Navegador de Directorios "
    pad   = "═" * max(0, cols - len(title) - 2)
    tokens = [
        ("class:frame.top", "╔"),
        ("class:frame.top", title),
        ("class:frame.top", pad),
        ("class:frame.top", "╗\n"),
    ]
    # Fila breadcrumb
    tokens += [("class:frame",  "║")]
    tokens += _breadcrumb(ruta, cols - 2)
    tokens += [("class:frame",  "║\n")]
    # Separador
    tokens += [
        ("class:frame", "╠"),
        ("class:frame", "═" * (cols - 2)),
        ("class:frame", "╣\n"),
    ]
    return tokens


def _render_lista(items, cursor, offset, visible, cols) -> list:
    tokens: list = []
    chunk  = items[offset : offset + visible]
    sbar   = _scrollbar(len(items), offset, visible)
    # ancho disponible para nombre: cols - 2(gutter) - 2(icono+sp) - 1(scrollbar)
    name_w = cols - 6

    if not chunk:
        pad = " " * (cols - 20)
        tokens.append(("class:item.name", f"   (directorio vacío){pad}\n"))
        return tokens

    for idx_rel, (ruta, ok) in enumerate(chunk):
        idx_abs = offset + idx_rel
        sel     = idx_abs == cursor
        sb_char = sbar[idx_rel]

        nombre = ruta.name
        if len(nombre) > name_w - 1:
            nombre = nombre[: name_w - 2] + "…"
        nombre_pad = nombre.ljust(name_w)

        if sel:
            tokens += [
                ("class:sel.pre",  "▌ "),
                ("class:sel.icon", " "),
                ("class:sel.name", f" {nombre_pad}"),
                ("class:scroll.thumb" if sb_char == "█" else "class:scroll.track",
                 sb_char + "\n"),
            ]
        elif not ok:
            tokens += [
                ("class:item.pre",  "  "),
                ("class:deny.icon", " "),
                ("class:deny.name", f" {nombre_pad}"),
                ("class:scroll.thumb" if sb_char == "█" else "class:scroll.track",
                 sb_char + "\n"),
            ]
        else:
            tokens += [
                ("class:item.pre",  "  "),
                ("class:item.icon", " "),
                ("class:item.name", f" {nombre_pad}"),
                ("class:scroll.thumb" if sb_char == "█" else "class:scroll.track",
                 sb_char + "\n"),
            ]
    return tokens


def _render_footer(total: int, cursor: int, cols: int) -> list:
    def k(t): return [("class:ft.key",   t)]
    def l(t): return [("class:ft.label", t)]
    sep = [("class:ft.sep", "  │  ")]

    # lado izquierdo — atajos
    left = (
        k("↑↓") + l(" nav") + sep +
        k("⏎")  + l(" entrar") + sep +
        k("←")  + l(" subir") + sep +
        k("SPC") + l(" confirmar") + sep +
        k("^C") + l(" salir")
    )
    left_len = sum(len(t[1]) for t in left) + 2  # +2 por padding

    # lado derecho — contador
    pos_str  = str(cursor + 1) if total > 0 else "0"
    cnt_str  = str(total)
    right_raw = f" {pos_str}/{cnt_str}  {total} items "
    right_len = len(right_raw) + 2

    mid_pad = " " * max(0, cols - left_len - right_len - 2)

    tokens = (
        [("class:ft.label", "  ")]
        + left
        + [("class:ft.label", mid_pad)]
        + [("class:ft.label",    "  ")]
        + [("class:ft.count",    f"{pos_str}")]
        + [("class:ft.label",    "/")]
        + [("class:ft.countval", f"{cnt_str}")]
        + [("class:ft.label",    f"   {total} items  \n")]
    )
    return tokens

# ─────────────────────────────────────────────────────────────────────────────
#  Función principal
# ─────────────────────────────────────────────────────────────────────────────
def navegador_directorios(ruta_inicial="."):
    resultado = [None]

    estado = {
        "ruta":     Path(ruta_inicial).resolve(),
        "items":    [],
        "cursor":   0,
        "offset":   0,
    }

    def _cargar(ruta):
        estado["ruta"]   = ruta
        estado["items"]  = _listar(ruta)
        estado["cursor"] = 0
        estado["offset"] = 0

    _cargar(estado["ruta"])

    def _scroll(delta):
        n = len(estado["items"])
        if n == 0:
            return
        cols, rows = _tsize()
        mv = _max_visible(rows)
        estado["cursor"] = max(0, min(n - 1, estado["cursor"] + delta))
        c, o = estado["cursor"], estado["offset"]
        if c < o:
            estado["offset"] = c
        elif c >= o + mv:
            estado["offset"] = c - mv + 1

    # ── Controles ────────────────────────────────────────────────────────────
    def _get_top():
        cols, _ = _tsize()
        return _render_top(estado["ruta"], cols)

    def _get_lista():
        cols, rows = _tsize()
        mv = _max_visible(rows)
        return _render_lista(
            estado["items"], estado["cursor"],
            estado["offset"], mv, cols
        )

    def _get_footer():
        cols, _ = _tsize()
        return _render_footer(
            len(estado["items"]), estado["cursor"], cols
        )

    layout = Layout(
        HSplit([
            Window(
                content=FormattedTextControl(_get_top),
                dont_extend_height=True,
            ),
            Window(
                content=FormattedTextControl(_get_lista),
            ),
            Window(
                content=FormattedTextControl(_get_footer),
                dont_extend_height=True,
                style="class:frame.bottom",
            ),
        ])
    )

    # ── Key bindings ─────────────────────────────────────────────────────────
    kb = KeyBindings()

    @kb.add("up")
    def _(e): _scroll(-1)

    @kb.add("down")
    def _(e): _scroll(+1)

    @kb.add("enter")
    def _(e):
        if not estado["items"]:
            return
        ruta_sel, ok = estado["items"][estado["cursor"]]
        if ok:
            _cargar(ruta_sel)

    @kb.add("left")
    def _(e):
        padre = estado["ruta"].parent
        if padre != estado["ruta"]:
            _cargar(padre)

    @kb.add("space")
    def _(e):
        resultado[0] = estado["ruta"]
        e.app.exit()

    @kb.add("c-c")
    def _(e):
        resultado[0] = None
        e.app.exit()

    # ── App ───────────────────────────────────────────────────────────────────
    app = Application(
        layout=layout,
        key_bindings=kb,
        style=STYLE,
        full_screen=False,
        mouse_support=False,
    )

    app.run()
    return resultado[0]


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    ruta = navegador_directorios(".")
    if ruta:
        print(f"\n\033[32m✔\033[0m  {ruta}")
    else:
        print("\n\033[31m✖\033[0m  Cancelado.")