"""
Modern Terminal UI for Crypto Messenger using Rich library.

This provides a colorful, formatted interface for encrypting and decrypting
messages using Caesar cipher. Features panels, tables, and styled prompts.

Installation: pip install rich
Usage: python rich_messenger.py
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich import box
from rich.text import Text
import caesar
import os

console = Console()


def main_menu():
    """Display rich main menu and handle user choices."""
    while True:
        console.clear()
        
        # Create title panel
        title = Panel.fit(
            "[bold cyan]🔐 CRYPTO MESSENGER[/bold cyan]\n"
            "[dim] Caesar Cipher Implementation[/dim]",
            border_style="cyan",
            padding=(1, 2)
        )
        console.print(title)
        console.print()
        
        # Create menu table
        table = Table(show_header=False, box=box.ROUNDED, border_style="blue", padding=(0, 2))
        table.add_column("Option", style="cyan bold", width=8)
        table.add_column("Description", style="white")
        
        table.add_row("1", "📤 Encrypt Message")
        table.add_row("2", "📥 Decrypt Message")
        table.add_row("3", "📄 View Message File")
        table.add_row("4", "🔄 ROT13 Demo")
        table.add_row("5", "❌ Exit")
        
        console.print(table)
        console.print()
        
        choice = Prompt.ask(
            "[bold yellow]Select option[/bold yellow]",
            choices=["1", "2", "3", "4", "5"],
            default="1"
        )
        
        if choice == "1":
            encrypt_workflow()
        elif choice == "2":
            decrypt_workflow()
        elif choice == "3":
            view_message_file()
        elif choice == "4":
            rot13_demo()
        elif choice == "5":
            console.print("\n[bold green]👋 Goodbye![/bold green]\n")
            break


def encrypt_workflow():
    """Rich encryption interface."""
    console.clear()
    
    # Header
    header = Panel(
        "[bold cyan]📤 ENCRYPT MESSAGE[/bold cyan]",
        border_style="cyan"
    )
    console.print(header)
    console.print()
    
    # Get message
    console.print("[yellow]Enter message to encrypt:[/yellow]")
    message = Prompt.ask("[dim]›[/dim]")
    
    if not message or not message.strip():
        console.print("\n[red]❌ Error: Message cannot be empty![/red]")
        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
        return
    
    # Get shift value
    shift = IntPrompt.ask(
        "[yellow]Enter shift[/yellow] [dim](press Enter for ROT13 default)[/dim]",
        default=caesar.DEFAULT_SHIFT
    )
    
    # Encrypt the message
    ciphertext = caesar.encrypt(message, shift)
    
    # Write to file
    try:
        with open("message.txt", "w") as f:
            f.write(f"v1.{ciphertext}")
        
        # Display result in panel
        result_text = Text()
        result_text.append("✅ Encrypted Successfully\n\n", style="green bold")
        result_text.append("Plaintext:  ", style="bold")
        result_text.append(f"{message}\n", style="white")
        result_text.append("Ciphertext: ", style="bold")
        result_text.append(f"{ciphertext}\n", style="yellow")
        result_text.append("Shift:      ", style="bold")
        result_text.append(f"{shift}\n", style="cyan")
        result_text.append("Saved to:   ", style="bold")
        result_text.append("message.txt", style="green")
        
        result_panel = Panel(
            result_text,
            border_style="green",
            padding=(1, 2)
        )
        console.print("\n")
        console.print(result_panel)
        
    except IOError as e:
        console.print(f"\n[red]❌ Error writing to message.txt: {e}[/red]")
    
    Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")


def decrypt_workflow():
    """Rich decryption interface."""
    console.clear()
    
    # Header
    header = Panel(
        "[bold cyan]📥 DECRYPT MESSAGE[/bold cyan]",
        border_style="cyan"
    )
    console.print(header)
    console.print()
    
    # Ask user for source of ciphertext
    console.print("[yellow]Decrypt from:[/yellow]")
    console.print("  [cyan]1[/cyan] - message.txt (saved file)")
    console.print("  [cyan]2[/cyan] - Enter ciphertext manually")
    console.print()
    
    choice = Prompt.ask(
        "[yellow]Select source[/yellow]",
        choices=["1", "2"],
        default="1"
    )
    
    console.print()
    
    # Get ciphertext based on choice
    if choice == "1":
        # Read from message.txt
        if not os.path.exists("message.txt"):
            console.print("[red]❌ No message.txt found![/red]")
            console.print("[dim]Encrypt a message first or choose manual entry.[/dim]")
            Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
            return
        
        try:
            with open("message.txt", "r") as f:
                content = f.read().strip()
            
            if not content:
                console.print("[red]❌ message.txt is empty![/red]")
                Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
                return
            
            # Strip version tag
            ciphertext = content[3:] if content.startswith("v1.") else content
            
            # Display the ciphertext
            cipher_panel = Panel(
                f"[yellow]{content}[/yellow]",
                title="[dim]From message.txt[/dim]",
                border_style="yellow",
                padding=(1, 2)
            )
            console.print(cipher_panel)
            console.print()
            
        except IOError as e:
            console.print(f"[red]❌ Error reading message.txt: {e}[/red]")
            Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
            return
    else:
        # Manual entry
        console.print("[yellow]Enter ciphertext to decrypt:[/yellow]")
        console.print("[dim](paste the encrypted message you received)[/dim]")
        user_input = Prompt.ask("[dim]›[/dim]")
        
        if not user_input or not user_input.strip():
            console.print("\n[red]❌ Ciphertext cannot be empty![/red]")
            Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
            return
        
        # Strip version tag if present
        ciphertext = user_input.strip()
        if ciphertext.startswith("v1."):
            ciphertext = ciphertext[3:]
        
        console.print()
    
    # Get shift key
    shift = IntPrompt.ask(
        "[yellow]Enter shift key[/yellow] [dim](press Enter for ROT13 default)[/dim]",
        default=caesar.DEFAULT_SHIFT
    )
    
    # Decrypt the message
    plaintext = caesar.decrypt(ciphertext, shift)
    
    # Display result
    result_text = Text()
    result_text.append("✅ Decrypted Successfully\n\n", style="green bold")
    result_text.append("Ciphertext: ", style="bold")
    result_text.append(f"{ciphertext}\n", style="yellow")
    result_text.append("Plaintext:  ", style="bold")
    result_text.append(f"{plaintext}\n", style="white")
    result_text.append("Shift:      ", style="bold")
    result_text.append(f"{shift}", style="cyan")
    
    result_panel = Panel(
        result_text,
        border_style="green",
        padding=(1, 2)
    )
    console.print("\n")
    console.print(result_panel)
    
    Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")


def view_message_file():
    """Display message file contents with syntax highlighting."""
    console.clear()
    
    # Header
    header = Panel(
        "[bold cyan]📄 MESSAGE FILE CONTENTS[/bold cyan]",
        border_style="cyan"
    )
    console.print(header)
    console.print()
    
    # Check if file exists
    if not os.path.exists("message.txt"):
        console.print("[red]❌ No message.txt found![/red]")
        console.print("[dim]The message file will be created when you encrypt a message.[/dim]")
        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
        return
    
    # Read and display file contents
    try:
        with open("message.txt", "r") as f:
            content = f.read().strip()
        
        if not content:
            console.print("[yellow]⚠️  message.txt exists but is empty[/yellow]")
        else:
            # Parse content
            if content.startswith("v1."):
                version = "v1"
                ciphertext = content[3:]
            else:
                version = "unknown"
                ciphertext = content
            
            # Create info table
            info_table = Table(show_header=False, box=box.SIMPLE, border_style="dim")
            info_table.add_column("Property", style="cyan")
            info_table.add_column("Value", style="white")
            
            info_table.add_row("File", "message.txt")
            info_table.add_row("Version", version)
            info_table.add_row("Length", f"{len(ciphertext)} characters")
            
            console.print(info_table)
            console.print()
            
            # Display ciphertext in panel
            file_panel = Panel(
                f"[yellow]{content}[/yellow]",
                title="[dim]Encrypted Content[/dim]",
                border_style="yellow",
                padding=(1, 2)
            )
            console.print(file_panel)
            
            console.print("\n[dim]This represents the insecure channel - readable but encrypted.[/dim]")
        
    except IOError as e:
        console.print(f"[red]❌ Error reading message.txt: {e}[/red]")
    
    Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")


def rot13_demo():
    """Interactive ROT13 demonstration with visualization."""
    console.clear()
    
    # Header
    header = Panel(
        "[bold cyan]🔄 ROT13 DEMONSTRATION[/bold cyan]\n"
        "[dim]ROT13 is self-inverse: encrypt(encrypt(x, 13), 13) = x[/dim]",
        border_style="cyan",
        padding=(1, 2)
    )
    console.print(header)
    console.print()
    
    # Get test message
    console.print("[yellow]Enter test message:[/yellow]")
    message = Prompt.ask("[dim]›[/dim]", default="HELLO WORLD")
    
    if not message.strip():
        console.print("\n[red]❌ Message cannot be empty![/red]")
        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
        return
    
    # Perform ROT13 encryption twice
    encrypted = caesar.encrypt(message, 13)
    decrypted = caesar.encrypt(encrypted, 13)  # ROT13 is self-inverse
    
    console.print()
    
    # Create visualization table
    demo_table = Table(
        show_header=True,
        box=box.ROUNDED,
        border_style="cyan",
        header_style="bold cyan",
        padding=(0, 2)
    )
    demo_table.add_column("Step", style="cyan bold", width=15)
    demo_table.add_column("Text", style="white", width=50)
    
    demo_table.add_row("Original", message)
    demo_table.add_row("ROT13 →", f"[yellow]{encrypted}[/yellow]")
    demo_table.add_row("ROT13 →", f"[green]{decrypted}[/green]")
    
    console.print(demo_table)
    console.print()
    
    # Verification message
    if message.upper() == decrypted:
        verification = Panel(
            "[green]✅ Self-inverse property verified![/green]\n\n"
            "[dim]The same ROT13 operation was used twice:\n"
            "1. Encrypt original → ciphertext\n"
            "2. Encrypt ciphertext → original\n\n"
            "This is why ROT13 is symmetric![/dim]",
            border_style="green",
            padding=(1, 2)
        )
        console.print(verification)
    else:
        console.print("[yellow]⚠️  Results differ due to case normalization[/yellow]")
    
    Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")


def main():
    """Entry point for the rich terminal UI."""
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠️  Interrupted by user[/yellow]")
        console.print("[bold green]👋 Goodbye![/bold green]\n")
    except Exception as e:
        console.print(f"\n[red]❌ Unexpected error: {e}[/red]\n")


if __name__ == "__main__":
    main()
