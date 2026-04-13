all:copy_file_path_extension.py
	mkdir -p ~/.local/share/nautilus-python/extensions
	cp copy_file_path_extension.py ~/.local/share/nautilus-python/extensions/
	nautilus -q
