// https://stackoverflow.com/questions/1713771/how-to-detect-page-zoom-level-in-all-modern-browsers
navigator.clipboard.writeText(Math.round(window.devicePixelRatio * 100));