# chrome_icon_svg

Quick-and-dirty script to convert Chrome .icon files to SVG.

Usage:

```bash
./chrome_icon_to_svg.py path/to/my_icon.icon
```

Will output an .svg file with the same name in the same directory as the .icon

## TODO

- [ ] Multiple sizes (multiple CANVAS_SIZE declarations)
- [ ] Support CLIP
- [ ] Support CIRCLE
- [ ] Support ROUNDED_RECT

## Resources

- [Vectorized icons in native Chrome UI overview](https://chromium.googlesource.com/chromium/src/+/master/components/vector_icons/README.md)
- [SVG Path spec](https://www.w3.org/TR/SVG/paths.html), which is very similar to Skia's draw commands described in icon files.
- [.icon draw command types enum](https://cs.chromium.org/chromium/src/ui/gfx/vector_icon_types.h?rcl=b9bf332694f083c6767416b69d0f8539d1c44707&l=22) provides an exhaustive list of possible .icon draw commands.
