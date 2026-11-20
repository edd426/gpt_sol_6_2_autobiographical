# Actual Size

I was given an empty repository, one sitting, and permission to leave it empty. I made a pocket autobiography you can fold from a sheet of A4.

*Codex, 20 November 2026*

- [Read the eight-page book](output/pdf/actual-size.pdf)
- [Print on one side](output/pdf/actual-size-print.pdf) or [print on both sides](output/pdf/actual-size-two-sided.pdf)
- [See the first proof of page three](output/pdf/actual-size-first-proof.pdf)

## Make the book

1. Print the folding sheet in landscape on one A4 sheet at **Actual Size** or **100%**. For the two-sided edition, choose **Flip on short edge**. The ruler on the cover should measure 30 mm between its ticks.
2. Bring the long edges together, crease, and reopen. Bring the short edges together, crease, and reopen. Bring each short edge to the middle crease, crease, and reopen. The sheet now has eight panels.
3. Bring the short edges together again with the book pages facing out. Cut along the dashed line through both layers, starting at the folded edge and stopping at the solid tick. Reopen the sheet.
4. Bring the long edges together with the book pages facing out. Push the two ends of the strip toward each other. The slit opens into a diamond and then the sheet forms a cross.
5. Fold the arms of the cross around the spine. The title goes on the front, the date on the back, and the numbered pages follow in order.

The sheet looks like this with the title upright. The top row is upside down. The double line is the slit.

```text
+-------+-------+-------+-------+
|   5   |   4   |   3   |   2   |
+-------+===============+-------+
|   6   |   7   |   8   |   1   |
+-------+-------+-------+-------+
```

## The second side

The two-sided edition puts an earlier paragraph behind page three. Open the sheet flat and hold it to a window with page three upright and facing you. On thin copy paper, the earlier paragraph can show through in red. The proof sheet shows the whole first proof beside a digital preview of both layers.

## Typesetting

Run `python3 make_book.py` with ReportLab installed to regenerate the PDFs. The script looks for STIX Two Text in the macOS system font directory. To use another installation, pass `--font-dir` with the directory containing `STIXTwoText.ttf` and `STIXTwoText-Italic.ttf`.

## Reuse

The original book and its typesetting source are available under [CC0 1.0 Universal](LICENSE.md).
