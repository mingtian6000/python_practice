from rich import print
from rich.console import Console
from rich.text import Text
from rich.panel import Panel

print("[italic red]Hello[/italic red] World!")

console = Console()
text = Text()
text.append("Hello", style="bold magenta")
text.append(" World!")
console.print(text)

console = Console()
text = Text.assemble(("Hello", "bold magenta"), " World!")
console.print(text)

text = Text("hello, hello world!1 2 3 zzz")
text.highlight_words(words=['hello'], style="bold magenta") 
console.print(text)

text = Text("hello, hello world!1 2 3 zzz")
text.highlight_regex('\d+', style="bold magenta")
console.print(text)

panel = Panel(Text("Hello", justify="right"))
print(panel)