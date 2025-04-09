"""
 ___________              __      _________.__  .__    .___         _________.__
\__    ___/___   _______/  |_   /   _____/|  | |__| __| _/____    /   _____/|  |__   ______  _  __
  |    |_/ __ \ /  ___/\   __\  \_____  \ |  | |  |/ __ |/ __ \   \_____  \ |  |  \ /  _ \ \/ \/ /
  |    |\  ___/ \___ \  |  |    /        \|  |_|  / /_/ \  ___/   /        \|   Y  (  <_> )     /
  |____| \___  >____  > |__|   /_______  /|____/__\____ |\___  > /_______  /|___|  /\____/ \/\_/
             \/     \/                 \/              \/    \/          \/      \/
                 .==.           We're Hiring: https://jobs.lever.co/.../
                ()''()-.
     .---.       ;--; /         Author: Lior Mizrahi
   .'_:___". _..'.  __'.        Source In GitHub: liormizr/<???>
   |__ --==|'-'''\\'...;
   [  ]  :[|      |---\\        Special Control Commands:
   |__| I=[|     .'    '.       * NEXT: >
   / / ____|     :       '._    * BACK: <
  |-/.____.'      | :       :   * PAGE-UP: <PAGEUP>
 /___\ /___\      '-'._----'    * PAGE-DOWN: <PAGEDOWN>
"""

from colorama import Fore, Style
from slides import BaseSlide


class FirstSlide(BaseSlide):
    """
    This is the first slide
    """


class SecondSlide(BaseSlide):
    """
    This is the second slide
    I know! {Style.BRIGHT}{Fore.YELLOW}💡{Style.RESET_ALL}
    {Style.BRIGHT}¯\_(ツ)_/¯
    """

    def code_snippet(self):
        print("Goodbye, World!")


class Questions(BaseSlide):
    """
    Questions?
    Thank you for your attention!
    Links:
    * ...
    * ...
    """

    def code_snippet(self):
        print("Hello, World!")
