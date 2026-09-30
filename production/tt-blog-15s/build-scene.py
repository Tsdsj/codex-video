from pathlib import Path
p=Path(__file__).resolve().parent
src=(p/'../../design/tt-blog-15s/keyframes.html').resolve().read_text()
src=src.replace('assets/','../../design/tt-blog-15s/assets/')
start=src.index('<script>');src=src[:start]+'''<style>
html,body{width:100%;height:100%;overflow:hidden;background:#09090b}header,.meta,.note{display:none!important}.board{margin:0;padding:0;max-width:none}.item{margin:0;position:absolute;inset:0}.holder{position:absolute;width:1600px;height:900px;overflow:visible;background:transparent}.frame{transform:none;opacity:0}.brand,.channel,.bottom{opacity:1}#stage{position:absolute;width:1600px;height:900px;transform-origin:top left}.intro .sphere{opacity:1}.intro .sphere img{display:none}.intro .mask{display:none}.sphere canvas{width:870px;height:680px}.frame .copy{will-change:transform,opacity}.end .center{will-change:opacity}#bridge{position:absolute;height:2px;background:#7cffb2;z-index:20;transform-origin:left center;pointer-events:none}
</style><script src="motion.js"></script></html>'''
(p/'scene.html').write_text(src)
