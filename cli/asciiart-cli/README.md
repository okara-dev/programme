# ASCII Art CLI

## What It Is

ASCII Art CLI is an interactive Node.js terminal tool for turning text and images into ASCII art. It supports ANSI colors, gradients, animations, and saving generated text to a file.

## Features

- Render text with Figlet fonts.
- Convert images to ASCII art with a configurable width.
- Apply single colors, horizontal or vertical rainbows, and gradients.
- Animate text with `typewriter`, `fade`, or `slide` styles.
- List fonts and save generated text to a UTF-8 file.

## Usage

```bash
npm install
npm start
```

For a global command: `npm link`, then run `asciiart`.

Inside the prompt:

```text
text "Hello" --font Big
rainbow "Hello world"
image ./logo.png --width 80
color "Warning" red
animate "Loading" typewriter
save "Release" release.txt --font Standard
```

Run `help` for the complete command list. Image conversion requires the optional `sharp` package used by the image renderer.

## Technology

- Node.js 14 or newer and ES modules
- `figlet` for text fonts
- ANSI terminal escape codes for color and animation

## Privacy and Safety

Text and image files are processed locally and are not sent to a remote service. The tool reads files you explicitly provide and writes output only when requested. Review generated files before sharing them.

## Distribution

ASCII Art CLI is distributed as a paid digital product through Gumroad. The Gumroad product page may contain the current package, release notes, and commercial purchase terms.

## License

The source project declares the MIT License. See `package.json` for project metadata. Gumroad purchase terms and the MIT License may apply to different parts of the distributed package; follow the terms included with your purchase.

## Status

Version 1.0.0. This is a terminal utility and is not intended to replace dedicated image or typography software.
