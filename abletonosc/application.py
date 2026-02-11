import Live
from typing import Tuple
from .handler import AbletonOSCHandler

class ApplicationHandler(AbletonOSCHandler):
    def init_api(self):
        #--------------------------------------------------------------------------------
        # Generic callbacks
        #--------------------------------------------------------------------------------
        def get_version(_) -> Tuple:
            application = Live.Application.get_application()
            return application.get_major_version(), application.get_minor_version()
        self.osc_server.add_handler("/live/application/get/version", get_version)
        self.osc_server.send("/live/startup")

        def get_average_process_usage(_) -> Tuple:
            application = Live.Application.get_application()
            return application.average_process_usage,
        self.osc_server.add_handler("/live/application/get/average_process_usage", get_average_process_usage)
        self.osc_server.send("/live/application/get/average_process_usage")

        #--------------------------------------------------------------------------------
        # Browser: List available items
        # Usage: /live/browser/get/items [category, (sub_category)]
        #   category: "instruments", "audio_effects", "midi_effects",
        #             "drums", "sounds", "packs", "samples"
        #   sub_category (optional): name of child to drill into
        # Returns: list of item names
        #--------------------------------------------------------------------------------
        def browser_get_items(params):
            app = Live.Application.get_application()
            browser = app.browser

            category_map = {
                "instruments": browser.instruments,
                "audio_effects": browser.audio_effects,
                "midi_effects": browser.midi_effects,
                "drums": browser.drums,
                "sounds": browser.sounds,
                "packs": browser.packs,
                "samples": browser.samples,
            }

            if len(params) < 1:
                return tuple(category_map.keys())

            category_name = str(params[0])
            category = category_map.get(category_name)
            if not category:
                return ("error", "unknown_category: %s" % category_name)

            parent = category
            for i in range(1, len(params)):
                sub_name = str(params[i])
                found = False
                for child in parent.children:
                    if child.name == sub_name:
                        parent = child
                        found = True
                        break
                if not found:
                    return ("error", "not_found: %s" % sub_name)

            names = []
            for child in parent.children:
                suffix = " *" if child.is_loadable else ""
                names.append(child.name + suffix)
            return tuple(names)

        self.osc_server.add_handler("/live/browser/get/items", browser_get_items)
