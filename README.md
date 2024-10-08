# Word Checker
Counts word occurrences in text files and results are saved in alphabetical order in a text file. Results are summarized for each source text file. Works best if the text files are saved as UTF-8 (with or without BOM), for example with Windows Notepad or Notepad++. The 3-byte BOM which can occur at the beginning of an UTF-8 file, is skipped so that the first word of the file is registered as a "normal word".

Some characters, especially commas, periods and parentheses after a word, are removed before a word is registered. This smoothes the vocabulary somewhat, but by keeping the punctuation inside of a word if any (such as "2.0"), typos such as missing spaces after a comma are also registered after a closing bracket. URLs or compositions with slashes are not split up so that low-level domains or word endings (such as the "s" in "file(s)") are not counted as separate words.

## Usage
`python WordOcc.py` 
At the first user prompt, insert a (relative) path, and any `*.txt` file inside that folder is scanned.<br>
On Windows, for example, entries such as C:\Users\FooBar\texte or ./subfolder1 both work fine.
Some rudimentary programmer mode for scanning (python) scripts is also implemented.

Multiple-term search: checking only the occurrence of multiple search terms defined by the user. To avoid coding misinterpretation of non-ASCII letters by the DOS command-line input, the search words cannot be entered at the command line but have to be stored in a UTF-8 text file in advance. Then run `python WordOcc.py /s` .

You can use the following command line arguments.

| Argument      | Description   |
| ------------- | ------------- |
| --help  or /?    | Display usage options              |
| --prog or /p     | Find words, commands and class objects in programming files |
| --refs or /r     | (under construction) gather words together with reference signs, such as `cable (17)` |
| --search or /s   | Only search for user-specified search terms |

Example:
```
python WordOcc.py --search
```

## Effect
Typos and inconsistencies in the used terms in large files can be easilier found. Such as inconsistency regarding hyphen usage or using similar terms, such as "disc" and "disk", for the same object.

## Next tasks
 * Some syntax highlighting for similar words

## Requirements
Written in Python 3 (works with e.g. version 3.8.1), these modules are imported: 
`sys, re, glob, os`

See also https://github.com/DGrothe-PhD/WordCheckerJava
<hr>

# German
Das Projekt enthält ein Python-Skript, das Wörter in Textdateien zählt. In einem Ordner gespeicherte Textdateien werden von Python ausgelesen und die ausgewerteten Wortlisten gespeichert. Die verwendeten Textdateien bleiben dabei unverändert. Kommen manche Wörter mehrfach vor, so erkennt man das an der Zahl. Die Zahl ist tabstoppgetrennt hinter dem jeweiligen Wort angegeben. Insofern kann eine solche Auswertung auch dazu dienen, die Wortliste weiterzuverarbeiten, indem man sie mit einer Spreadsheet-Anwendung, z. B. Excel, öffnet, wo das Ergebnis dann weiter analysiert werden kann.

## Zielsetzung

Es soll eine Schnelldurchsicht nach verwendeten Wörtern ermöglicht werden. Uneinheitlichkeiten (denselben Begriff mal mit Bindestrich und mal ohne) oder Tippfehler sowie OCR-Erkennungsfehler lassen sich leichter auffinden.

## Funktionsweise

Es werden einige Zeichen, vor allem Kommas, Punkte sowie außen stehende Klammern, entfernt, bevor ein Wort registriert wird. Dies glättet den Wortschatz etwas, durch Beibehaltung der Zeichen, die im Wort auftauchen, werden allerdings auch Tippfehler wie fehlende Leerzeichen nach einer schließenden Klammer registriert. Andererseits werden auch die URLs unverändert belassen, damit etwa Low-Level-Domains nicht als Einzelwortbrocken mitzählen.

Um auch europäische Sprachen außer Englisch verwenden zu können, speichert man die Textdateien am besten im UTF-8-Format, dies ermöglicht der Windows bekannte Editor in den heutigen Windows-Versionen üblicherweise durch einen einfachen Mausklick. Apostrophs und Wörter mit Nicht-ASCII-Buchstaben (étagère, ça) sollten so ebenfalls korrekt verarbeitet werden.

Siehe auch https://github.com/DGrothe-PhD/WordCheckerJava
