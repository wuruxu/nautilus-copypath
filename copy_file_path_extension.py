import gi

gi.require_version("Gdk", "4.0")
gi.require_version("Nautilus", "4.1")

from gi.repository import GObject, Gdk, Nautilus


class CopyFilePathExtension(GObject.GObject, Nautilus.MenuProvider):
    def get_file_items(self, files):
        local_paths = [file.get_location().get_path() for file in files if file.get_location()]
        local_paths = [path for path in local_paths if path]

        if not local_paths:
            return

        label = "Copy File Path" if len(local_paths) == 1 else "Copy File Paths"
        item = Nautilus.MenuItem(
            name="CopyFilePathExtension::CopyFilePath",
            label=label,
            tip="Copy the selected file path to the clipboard",
        )
        item.connect("activate", self._copy_to_clipboard, local_paths)
        return (item,)

    def _copy_to_clipboard(self, menu_item, local_paths):
        text = "\n".join(self._format_path(path) for path in local_paths)
        self._copy_with_gdk(text)

    def _copy_with_gdk(self, text):
        display = Gdk.Display.get_default()
        if display is None:
            return

        value = GObject.Value()
        value.init(str)
        value.set_string(text)
        display.get_clipboard().set(value)

    def _format_path(self, path):
        if " " in path:
            return f"'{path}'"
        return path
