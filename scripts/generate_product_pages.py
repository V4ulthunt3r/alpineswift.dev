#!/usr/bin/env python3
"""Writes the static product pages /trail/, /scout/, /beacon/ (DE) and /en/... (EN).
Usage: python3 scripts/generate_product_pages.py .   (run from the repo root, then commit the HTML)
The output is plain HTML; the site itself has no build step."""
import os, sys

ROOT = sys.argv[1]
SITE = "https://alpineswift.dev"
MAIL = "info@hildel.com"

ICONS = {
    "trail": ("/assets/img/tools/trail-light.svg", "/assets/img/tools/trail-dark.svg"),
    "scout": ("/assets/img/tools/scout-light.jpg", "/assets/img/tools/scout-dark.jpg"),
    "beacon": ("/assets/img/tools/beacon-light.jpg", "/assets/img/tools/beacon-dark.jpg"),
}
ORDER = ["trail", "scout", "beacon"]
NAMES = {"trail": "Trail", "scout": "Scout", "beacon": "Beacon"}

UI = {
    "de": {
        "home": "/", "prefix": "", "fid": "funktionen", "cid": "interesse", "other": "en", "other_label": "EN", "other_lang_name": "English",
        "studio": "Studio", "interest": "Interesse melden", "menu": "Menü", "nav_label": "Hauptnavigation",
        "brand_label": "Alpine Swift, zur Startseite",
        "theme_label": "Farbschema: Automatisch (System). Wechseln",
        "icon_alt": "App-Icon von {n}", "tools_of": "Werkzeug {i} / 03",
        "why": "Warum {n}", "features": "Funktionen", "features_h": "Was {n} kann.",
        "principles_label": "Für alle drei Werkzeuge",
        "principles_h": "Gebaut wie unsere Apps.",
        "spec_label": "Steckbrief", "spec_h": "{n} auf einen Blick.",
        "team_label": "Die Seilschaft", "team_h": "Drei Werkzeuge, eine Route.",
        "team_p": "Trail plant, Scout prüft, Beacon bringt die App in den Store. Jedes Werkzeug funktioniert für sich, zusammen decken sie den Weg vom ersten Ticket bis zum fertigen Store-Eintrag ab.",
        "here": "Du bist hier",
        "cta_label": "Interesse",
        "copy": "Adresse kopieren", "copied": "Kopiert",
        "back": "Du brauchst eine App statt eines Werkzeugs? <a href=\"/#kontakt\">Zum App-Studio</a>",
        "legal_label": "Rechtliches", "imprint": "Impressum", "privacy": "Datenschutz",
        "locale": "de_DE",
        "principles": [
            ("Lokal zuerst", "Deine Daten liegen auf deinen Geräten. Kein Konto bei Alpine Swift und kein eigener Server dazwischen."),
            ("Nativ für Apple", "Gebaut mit Swift und SwiftUI, mit Hell- und Dunkelmodus und den Bedienmustern, die du von Apple kennst."),
            ("Assistenten willkommen", "Jedes Werkzeug bringt eine lokale MCP-Schnittstelle mit. KI-Assistenten dürfen lesen, prüfen und vorschlagen."),
            ("Du entscheidest", "Übernommen, veröffentlicht oder eingereicht wird nur, was du selbst bestätigt hast. Kein stiller Automatismus."),
        ],
    },
    "en": {
        "home": "/en/", "prefix": "/en", "fid": "features", "cid": "interest", "other": "de", "other_label": "DE", "other_lang_name": "Deutsch",
        "studio": "Studio", "interest": "Register interest", "menu": "Menu", "nav_label": "Main navigation",
        "brand_label": "Alpine Swift, to the home page",
        "theme_label": "Colour scheme: Automatic (system). Change",
        "icon_alt": "{n} app icon", "tools_of": "Tool {i} / 03",
        "why": "Why {n}", "features": "Features", "features_h": "What {n} does.",
        "principles_label": "Shared by all three tools",
        "principles_h": "Built like our apps.",
        "spec_label": "Fact sheet", "spec_h": "{n} at a glance.",
        "team_label": "The rope team", "team_h": "Three tools, one route.",
        "team_p": "Trail plans, Scout checks, Beacon takes the app to the store. Each tool works on its own; together they cover the way from the first ticket to a finished store listing.",
        "here": "You are here",
        "cta_label": "Interest",
        "copy": "Copy address", "copied": "Copied",
        "back": "Need an app rather than a tool? <a href=\"/en/#contact\">Visit the app studio</a>",
        "legal_label": "Legal", "imprint": "Imprint", "privacy": "Privacy",
        "locale": "en_US",
        "principles": [
            ("Local first", "Your data lives on your devices. No Alpine Swift account and no server of ours in between."),
            ("Native to Apple", "Built with Swift and SwiftUI, with light and dark mode and the interaction patterns you know from Apple."),
            ("Assistants welcome", "Every tool ships a local MCP interface. AI assistants may read, check and suggest."),
            ("You decide", "Nothing is applied, published or submitted unless you confirmed it yourself. No silent automation."),
        ],
    },
}

P = {
    "trail": {
        "rot": 0,
        "path": "M-10 410 C 40 360, 30 320, 90 300 S 150 250, 128 214",
        "de": {
            "title": "Trail · Projektmanagement für Indie-Entwickler · Alpine Swift",
            "desc": "Trail ist natives, lokales Projektmanagement für iPhone, iPad und Mac: Aufgaben, Meilensteine, Notizen und Dateien an einem Ort, synchronisiert über deine eigene iCloud. Ein Werkzeug von Alpine Swift.",
            "label": "Werkzeug 01 · Planen",
            "tagline": "Die Route für deine <em>App-Projekte.</em>",
            "lede": "Trail ist Projektmanagement für Indie-Entwickler: Aufgaben, Meilensteine, Notizen und Dateien an einem Ort, nativ auf iPhone, iPad und Mac. Deine Daten liegen auf deinen Geräten und gleichen sich über deine eigene iCloud ab.",
            "status": ("live", "Intern im Einsatz"),
            "platforms": ["iPhone", "iPad", "Mac"],
            "corner": "Etappe · alle",
            "meta": "Planen · alle Etappen",
            "short": "Projekte, Aufgaben und Entscheidungen festhalten.",
            "why_h": "Gebaut für Projekte mit einer Person an Bord.",
            "why_p": "Große Projekt-Tools sind für Teams mit Rollen, Sprints und Lizenzen gedacht. Wer allein oder zu zweit Apps baut, braucht etwas anderes: schnell erfasst, offline verfügbar und nah am Code.",
            "why": [
                ("Schnell erfasst", "Eingang, Heute und Meine Aufgaben: Ideen landen sofort im richtigen Projekt und tauchen wieder auf, wenn sie dran sind."),
                ("Nah am Code", "Issues, Branches, Pull Requests und Commits aus GitHub hängen direkt an der Aufgabe, zu der sie gehören."),
                ("Ohne fremden Server", "Synchronisiert wird über deine private iCloud. Es gibt kein Konto bei Alpine Swift und keine Projektdaten auf unseren Rechnern."),
            ],
            "features": [
                ("Liste oder Board", "Jedes Projekt als Liste oder Kanban-Board mit frei konfigurierbaren Statusspalten. Aufgaben per Drag-and-drop verschieben und sortieren."),
                ("Meilensteine und Abhängigkeiten", "Unteraufgaben, Checklisten, Tags, Meilensteine und Abhängigkeiten, die keine Kreise zulassen. Dazu geschätzter und tatsächlicher Aufwand."),
                ("Zeitleiste und Kennzahlen", "Planungskennzahlen und eine Zeitleiste zeigen, ob das Projekt auf Kurs ist, bevor der Zieltermin drückt."),
                ("Notizen mit Versionen", "Konzepte und Entscheidungen als versionierte Notizen direkt im Projekt. Frühere Stände bleiben nachvollziehbar."),
                ("Dateien am richtigen Ort", "Entwürfe, Screenshots und Dokumente gehören zum Projekt, zur Aufgabe oder zur Notiz. Mit Typfilter und Quick Look, Originale werden mit Prüfsumme gesichert."),
                ("Eine Suche für alles", "Projekte und Aufgaben in einer Suche, filterbar nach Favoriten, Status, Priorität und Fälligkeit."),
            ],
            "assist": "Auf dem Mac bringt Trail den lokalen Adapter <code>trail-mcp</code> mit. Gibst du ein Projekt frei, kann ein KI-Assistent es lesen, Titel und Termine prüfen und Verbesserungen vorschlagen. Übernommen wird erst, wenn du im Review zustimmst. Die Freigabe endet, sobald du sie widerrufst oder Trail beendest.",
            "spec": [
                ("Plattformen", "iPhone und iPad ab iOS 18, Mac ab macOS 15", ""),
                ("Daten und Sync", "Lokal gespeichert, Abgleich über deine private iCloud (CloudKit)", "Änderungen bleiben auch offline erhalten und werden beim nächsten Abgleich zusammengeführt."),
                ("Anbindungen", "GitHub: Issues, Branches, Pull Requests und Commits", "Lokale KI-Assistenten über MCP (Mac)"),
                ("Stand", "Bei jedem Alpine-Swift-Projekt im Einsatz", "Eine Veröffentlichung im App Store ist geplant, aber noch nicht terminiert."),
            ],
            "cta_h": "Sag Bescheid, wenn du Trail testen willst.",
            "cta_p": "Trail ist noch nicht öffentlich. Schreib mir kurz, woran du arbeitest. Sobald eine Testphase startet, melde ich mich. Kein Newsletter, nur eine Mail, wenn es so weit ist.",
            "subject": "Interesse an Trail",
        },
        "en": {
            "title": "Trail · Project management for indie developers · Alpine Swift",
            "desc": "Trail is native, local-first project management for iPhone, iPad and Mac: tasks, milestones, notes and files in one place, synced through your own iCloud. A tool by Alpine Swift.",
            "label": "Tool 01 · Plan",
            "tagline": "The route for your <em>app projects.</em>",
            "lede": "Trail is project management for indie developers: tasks, milestones, notes and files in one place, native on iPhone, iPad and Mac. Your data stays on your devices and syncs through your own iCloud.",
            "status": ("live", "In use in-house"),
            "platforms": ["iPhone", "iPad", "Mac"],
            "corner": "Stage · all",
            "meta": "Plan · every stage",
            "short": "Keep projects, tasks and decisions on record.",
            "why_h": "Built for projects with one person on board.",
            "why_p": "Big project tools are made for teams with roles, sprints and seat licences. If you build apps on your own or as a pair, you need something else: quick to capture, available offline and close to the code.",
            "why": [
                ("Quick to capture", "Inbox, Today and My Tasks: ideas land in the right project straight away and come back when it is their turn."),
                ("Close to the code", "Issues, branches, pull requests and commits from GitHub sit right on the task they belong to."),
                ("No third-party server", "Sync runs through your private iCloud. There is no Alpine Swift account and no project data on our machines."),
            ],
            "features": [
                ("List or board", "Every project as a list or a Kanban board with fully configurable status columns. Move and reorder tasks with drag and drop."),
                ("Milestones and dependencies", "Subtasks, checklists, tags, milestones and dependencies that never allow a cycle. Plus estimated and actual effort."),
                ("Timeline and metrics", "Planning metrics and a timeline show whether the project is on track before the deadline starts to bite."),
                ("Versioned notes", "Concepts and decisions as versioned notes right inside the project. Earlier versions stay traceable."),
                ("Files where they belong", "Drafts, screenshots and documents belong to the project, a task or a note. With type filters and Quick Look; originals are stored with a checksum."),
                ("One search for everything", "Projects and tasks in a single search, filtered by favourites, status, priority and due date."),
            ],
            "assist": "On the Mac, Trail ships the local adapter <code>trail-mcp</code>. Once you share a project, an AI assistant can read it, check titles and dates and suggest improvements. Nothing is applied until you approve it in the review. Sharing ends as soon as you revoke it or quit Trail.",
            "spec": [
                ("Platforms", "iPhone and iPad on iOS 18 or later, Mac on macOS 15 or later", ""),
                ("Data and sync", "Stored locally, synced through your private iCloud (CloudKit)", "Changes survive offline and are merged on the next sync."),
                ("Integrations", "GitHub: issues, branches, pull requests and commits", "Local AI assistants via MCP (Mac)"),
                ("Status", "In use on every Alpine Swift project", "An App Store release is planned, but not yet scheduled."),
            ],
            "cta_h": "Let me know if you want to try Trail.",
            "cta_p": "Trail is not public yet. Drop me a line about what you are working on. As soon as a test phase starts, I will get in touch. No newsletter, just one email when it is time.",
            "subject": "Interested in Trail",
        },
    },
    "scout": {
        "rot": 120,
        "path": "M410 410 C 360 380, 370 330, 310 320 S 260 290, 272 250",
        "de": {
            "title": "Scout · Qualitätsprüfung für Swift-Projekte · Alpine Swift",
            "desc": "Scout prüft Swift- und SwiftUI-Projekte vor dem Release: SwiftLint, Build, Tests und Coverage in einem Lauf, lokal auf dem Mac, mit Verlauf und Berichten. Ein Werkzeug von Alpine Swift.",
            "label": "Werkzeug 02 · Prüfen",
            "tagline": "Der Qualitätscheck <em>vor jedem Release.</em>",
            "lede": "Scout prüft deine Swift- und SwiftUI-Projekte, bevor sie in den Store gehen: Lint-Regeln, Build, Tests und Coverage in einem Lauf, lokal auf deinem Mac. Am Ende steht ein Bericht, der zeigt, was besser geworden ist und was noch fehlt.",
            "status": ("live", "Intern im Einsatz"),
            "platforms": ["Mac", "Xcode", "SwiftLint"],
            "corner": "Etappe 2 · Native App",
            "meta": "Prüfen · Etappe 2",
            "short": "Code vor dem Release auf Qualität prüfen.",
            "why_h": "Wenn KI mitschreibt, muss jemand gegenlesen.",
            "why_p": "KI-Werkzeuge liefern schnell viel Code. Ob er sauber, getestet und wartbar ist, zeigt sich oft erst nach dem Launch. Scout macht das vorher sichtbar, ohne dass dein Code den Rechner verlässt.",
            "why": [
                ("Ein Lauf, alle Prüfungen", "SwiftLint, Build, Tests und gemessene Coverage aus deinen Xcode-Schemes. Kein Zusammensuchen aus vier Terminalfenstern."),
                ("Fortschritt statt Momentaufnahme", "Jeder Lauf wird gespeichert. Scout vergleicht mit einem gewählten Ausgangsstand und zeigt, welche Befunde neu sind und welche erledigt."),
                ("Lokal und belegbar", "Prüfsummen vor und nach jedem Lauf belegen, welcher Quellstand geprüft wurde. Der Code bleibt auf deinem Mac."),
            ],
            "features": [
                ("Prüfprofile aus Xcode", "Schemes, Konfigurationen und Testziele liest Scout aus dem Projekt und speichert sie als wiederverwendbares Prüfprofil."),
                ("Eigene Regeln", "Standardregeln ein- und ausschalten, eigene Regex-Regeln mit Meldung und Schweregrad anlegen, Pfade ausschließen. Ohne die Projektdateien anzufassen."),
                ("Best-Practice-Katalog", "Empfehlungen für Swift und SwiftUI mit Quellen und klar benannten Prüfgrenzen. Ausgewählte Regeln laufen als Zusatzprüfung pro Projekt."),
                ("Befunde, die mitwandern", "Verschiebt sich Code, ordnet Scout unveränderte Befundzeilen über gespeicherte Hashes wieder zu. Der Vergleich bleibt aussagekräftig."),
                ("Berichte für Menschen und Agents", "Export als HTML zum Lesen und als JSON für Werkzeuge, dazu eine Markdown-Anleitung, wie der Bericht zu lesen ist."),
                ("KI-Reparaturauftrag", "Aus einem Prüflauf wird ein fertiger Prompt: kopieren oder als Markdown-Datei speichern und deinem Coding-Assistenten übergeben."),
            ],
            "assist": "Über den eingebetteten Adapter <code>scout-mcp</code> sieht ein lokaler Assistent Profile und Kennzahlen eines freigegebenen Projekts und kann Regeländerungen vorschlagen. Quelltexte und Kontodaten gibt Scout nicht heraus, und eine Regel ändert sich erst, wenn du den Vorschlag in Scout annimmst.",
            "spec": [
                ("Plattform", "Mac ab macOS 26", ""),
                ("Prüft", "Swift- und SwiftUI-Projekte mit Xcode", "SwiftLint, Build, Tests und Coverage über xcodebuild"),
                ("Anbindungen", "Lokale KI-Assistenten über MCP", "GitHub-Anbindung für Branch- und Commit-Nachweise in Vorbereitung"),
                ("Stand", "Bei jedem Alpine-Swift-Projekt im Einsatz, Version 1 in Fertigstellung", "Eine Veröffentlichung ist geplant, aber noch nicht terminiert."),
            ],
            "cta_h": "Sag Bescheid, wenn du Scout testen willst.",
            "cta_p": "Scout ist noch nicht öffentlich. Schreib mir kurz, an welchem Swift-Projekt du arbeitest. Sobald eine Testphase startet, melde ich mich. Kein Newsletter, nur eine Mail, wenn es so weit ist.",
            "subject": "Interesse an Scout",
        },
        "en": {
            "title": "Scout · Quality checks for Swift projects · Alpine Swift",
            "desc": "Scout checks Swift and SwiftUI projects before release: SwiftLint, build, tests and coverage in one run, locally on the Mac, with history and reports. A tool by Alpine Swift.",
            "label": "Tool 02 · Check",
            "tagline": "The quality check <em>before every release.</em>",
            "lede": "Scout checks your Swift and SwiftUI projects before they go to the store: lint rules, build, tests and coverage in one run, locally on your Mac. You end up with a report that shows what got better and what is still missing.",
            "status": ("live", "In use in-house"),
            "platforms": ["Mac", "Xcode", "SwiftLint"],
            "corner": "Stage 2 · Native app",
            "meta": "Check · stage 2",
            "short": "Check code quality before every release.",
            "why_h": "When AI writes along, someone has to proofread.",
            "why_p": "AI tools produce a lot of code, fast. Whether it is clean, tested and maintainable often only shows after launch. Scout makes it visible beforehand, without your code ever leaving your machine.",
            "why": [
                ("One run, every check", "SwiftLint, build, tests and measured coverage from your Xcode schemes. No piecing results together from four terminal windows."),
                ("Progress, not a snapshot", "Every run is saved. Scout compares against a baseline you choose and shows which findings are new and which are resolved."),
                ("Local and provable", "Checksums before and after every run prove which source state was checked. The code stays on your Mac."),
            ],
            "features": [
                ("Profiles from Xcode", "Scout reads schemes, configurations and test destinations from the project and saves them as a reusable check profile."),
                ("Your own rules", "Turn default rules on and off, add custom regex rules with message and severity, exclude paths. Without touching project files."),
                ("Best-practice catalogue", "Recommendations for Swift and SwiftUI with sources and clearly stated limits. Selected rules run as an extra check per project."),
                ("Findings that move with the code", "When code shifts, Scout re-matches unchanged finding lines through stored hashes. The comparison stays meaningful."),
                ("Reports for people and agents", "Export as HTML for reading and JSON for tools, plus a Markdown guide on how to read the report."),
                ("AI repair brief", "A check run becomes a ready-made prompt: copy it or save it as a Markdown file and hand it to your coding assistant."),
            ],
            "assist": "Through the embedded adapter <code>scout-mcp</code>, a local assistant sees the profiles and metrics of a shared project and can propose rule changes. Scout never hands out source code or account data, and a rule only changes once you accept the proposal in Scout.",
            "spec": [
                ("Platform", "Mac on macOS 26 or later", ""),
                ("Checks", "Swift and SwiftUI projects built with Xcode", "SwiftLint, build, tests and coverage via xcodebuild"),
                ("Integrations", "Local AI assistants via MCP", "GitHub link for branch and commit evidence in preparation"),
                ("Status", "In use on every Alpine Swift project, version 1 nearing completion", "A release is planned, but not yet scheduled."),
            ],
            "cta_h": "Let me know if you want to try Scout.",
            "cta_p": "Scout is not public yet. Drop me a line about the Swift project you are working on. As soon as a test phase starts, I will get in touch. No newsletter, just one email when it is time.",
            "subject": "Interested in Scout",
        },
    },
    "beacon": {
        "rot": 240,
        "path": "M200 -10 C 240 30, 190 60, 230 90 S 210 110, 200 116",
        "de": {
            "title": "Beacon · App-Store-Metadaten und ASO für Indie-Entwickler · Alpine Swift",
            "desc": "Beacon ist ein nativer Arbeitsplatz für deinen App-Store-Auftritt: Texte, Keywords, Screenshots, Releases und Bewertungen an einem Ort, verbunden mit App Store Connect. Ein Werkzeug von Alpine Swift.",
            "label": "Werkzeug 03 · Veröffentlichen",
            "tagline": "Dein App-Store-Auftritt <em>an einem Ort.</em>",
            "lede": "Beacon ist ein Arbeitsplatz für alles, was im App Store sichtbar ist: Texte, Keywords, Screenshots, Versionen und Bewertungen. Nativ auf dem Mac, dazu iPhone und iPad, verbunden mit App Store Connect über deinen eigenen Zugang.",
            "status": ("dev", "In Entwicklung"),
            "platforms": ["Mac", "iPhone", "iPad"],
            "corner": "Etappe 3 · Launch &amp; Betrieb",
            "meta": "Veröffentlichen · Launch &amp; Betrieb",
            "short": "Store-Eintrag pflegen, Releases einreichen.",
            "why_h": "App Store Connect ist ein Formular-Labyrinth.",
            "why_p": "Mehrere Sprachen, mehrere Gerätegrößen, regelmäßige Updates: Wer seinen Store-Eintrag pflegt, klickt sich durch Dutzende Formulare und verliert leicht den Überblick, was wann geändert wurde und ob es etwas gebracht hat.",
            "why": [
                ("Alles an einem Ort", "Metadaten, Screenshots, Releases und Bewertungen in einer App statt verteilt über viele Seiten."),
                ("Erst Entwurf, dann live", "Änderungen entstehen lokal als Entwurf. Zu Apple geht nur, was du einzeln geprüft und bestätigt hast."),
                ("Lernen statt raten", "Ein ASO-Journal hält fest, was du geändert hast und warum, und vergleicht die Downloads vorher und nachher."),
            ],
            "features": [
                ("Metadaten und Sprachen", "Store-Texte und Keywords aller Sprachen nebeneinander, mit Prüfung der Zeichen- und Byte-Grenzen, bevor etwas zu Apple geht."),
                ("Screenshot Studio", "Screenshots importieren, pro Sprache und Gerät ordnen und gegen Apples aktuelle Vorgaben prüfen, bevor sie hochgeladen werden."),
                ("Release Center", "Pro Version ein Arbeitsbereich: Build zuordnen, Release Notes schreiben, Pflichtfelder prüfen und zur App-Prüfung einreichen. Jeder Schritt einzeln bestätigt."),
                ("Bewertungen und Antworten", "Rezensionen nach Sternen, Ländern und unbeantwortet filtern, Antworten als Entwurf vorbereiten und bewusst veröffentlichen."),
                ("ASO-Auswertung", "Downloads nach Land, Quelle und Gerät über 7, 28 und 90 Tage. Dazu Maßnahmen mit Hypothese, Ziel und Vorher-nachher-Vergleich."),
                ("Optionaler KI-Assistent", "Auf dem Gerät mit Apple Intelligence oder mit deinem eigenen OpenAI-Schlüssel. Vorschläge mit Quellenangabe, übernommen wird erst nach deiner Prüfung."),
            ],
            "assist": "Über den lokalen MCP-Server kann ein Assistent ausdrücklich freigegebene Metadaten lesen, Keywords analysieren und Änderungen vorbereiten. Veröffentlichen, einreichen oder Zugangsdaten lesen kann er nicht. Jeder Vorschlag braucht deine Annahme in Beacon.",
            "spec": [
                ("Plattformen", "Mac ab macOS 15, iPhone und iPad ab iOS 26", ""),
                ("Anbindungen", "App Store Connect über deinen eigenen API-Zugang", "GitHub, Fastlane-Metadaten und lokale KI-Assistenten über MCP"),
                ("KI", "Optional: Apple Intelligence auf dem Gerät oder eigener OpenAI-Schlüssel", "Kein automatischer Wechsel zwischen Anbietern, keine automatische Übernahme"),
                ("Stand", "In Entwicklung", "Heute pflegt Alpine Swift Store-Einträge noch von Hand, Beacon soll das ablösen. Eine Veröffentlichung ist geplant, aber noch nicht terminiert."),
            ],
            "cta_h": "Sag Bescheid, wenn du Beacon testen willst.",
            "cta_p": "Beacon ist noch in Entwicklung. Schreib mir kurz, welche Apps du im Store pflegst. Sobald eine Testphase startet, melde ich mich. Kein Newsletter, nur eine Mail, wenn es so weit ist.",
            "subject": "Interesse an Beacon",
        },
        "en": {
            "title": "Beacon · App Store metadata and ASO for indie developers · Alpine Swift",
            "desc": "Beacon is a native workspace for your App Store presence: copy, keywords, screenshots, releases and reviews in one place, connected to App Store Connect. A tool by Alpine Swift.",
            "label": "Tool 03 · Publish",
            "tagline": "Your App Store presence <em>in one place.</em>",
            "lede": "Beacon is a workspace for everything people see in the App Store: copy, keywords, screenshots, versions and reviews. Native on the Mac, plus iPhone and iPad, connected to App Store Connect through your own access.",
            "status": ("dev", "In development"),
            "platforms": ["Mac", "iPhone", "iPad"],
            "corner": "Stage 3 · Launch &amp; care",
            "meta": "Publish · launch &amp; care",
            "short": "Maintain your listing, submit releases.",
            "why_h": "App Store Connect is a maze of forms.",
            "why_p": "Several languages, several device sizes, regular updates: keeping a store listing current means clicking through dozens of forms, and it is easy to lose track of what changed when and whether it made any difference.",
            "why": [
                ("Everything in one place", "Metadata, screenshots, releases and reviews in one app instead of spread across many pages."),
                ("Draft first, then live", "Changes start as local drafts. Only what you reviewed and confirmed one by one goes to Apple."),
                ("Learn, don't guess", "An ASO journal records what you changed and why, and compares downloads before and after."),
            ],
            "features": [
                ("Metadata and languages", "Store copy and keywords for every language side by side, with character and byte limits checked before anything goes to Apple."),
                ("Screenshot Studio", "Import screenshots, arrange them per language and device and check them against Apple's current specs before uploading."),
                ("Release Center", "One workspace per version: assign a build, write release notes, check required fields and submit for App Review. Every step confirmed on its own."),
                ("Reviews and replies", "Filter reviews by stars, territory and unanswered, prepare replies as drafts and publish them deliberately."),
                ("ASO analytics", "Downloads by territory, source and device over 7, 28 and 90 days. Plus actions with hypothesis, goal and a before/after comparison."),
                ("Optional AI assistant", "On-device with Apple Intelligence or with your own OpenAI key. Suggestions cite their sources and are only applied after your review."),
            ],
            "assist": "Through its local MCP server, an assistant can read explicitly shared metadata, analyse keywords and prepare changes. It cannot publish, submit or read credentials. Every proposal needs your acceptance in Beacon.",
            "spec": [
                ("Platforms", "Mac on macOS 15 or later, iPhone and iPad on iOS 26 or later", ""),
                ("Integrations", "App Store Connect through your own API access", "GitHub, Fastlane metadata and local AI assistants via MCP"),
                ("AI", "Optional: on-device Apple Intelligence or your own OpenAI key", "No automatic provider fallback, no automatic acceptance"),
                ("Status", "In development", "Today Alpine Swift still maintains store listings by hand; Beacon is meant to replace that. A release is planned, but not yet scheduled."),
            ],
            "cta_h": "Let me know if you want to try Beacon.",
            "cta_p": "Beacon is still in development. Drop me a line about the apps you maintain in the store. As soon as a test phase starts, I will get in touch. No newsletter, just one email when it is time.",
            "subject": "Interested in Beacon",
        },
    },
}

MARK = """<svg viewBox="70 100 1085 1010" aria-hidden="true">
        <path class="mk-mtn" d="M88 1095 L617 621 L1068 1050 L665 740 L567 925 L509 862 Z"/>
        <path class="mk-facet" d="M665 740 L1068 1050 L722 900 Z"/>
        <g class="mk-bird"><path d="M647 118 C700 225 820 350 975 402 C1000 390 1030 376 1058 377 C1074 378 1084 386 1088 393 L1106 401 C1082 403 1061 412 1047 429 C1040 440 1036 452 1035 461 C1100 540 1150 680 1135 812 C1115 690 1050 582 945 515 C870 545 800 585 737 628 L823 533 L678 546 C740 530 800 510 850 487 L875 463 C760 380 660 255 647 118 Z"/><path class="mk-wing" d="M1135 812 C1115 690 1050 582 945 515 L988 503 C1062 562 1116 664 1135 812 Z"/></g>
      </svg>"""

THEME_ICON = """<svg viewBox="0 0 20 20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><g class="ti-auto"><circle cx="10" cy="10" r="7"/><path d="M10 3a7 7 0 0 0 0 14z" fill="currentColor" stroke="none"/></g><g class="ti-light"><circle cx="10" cy="10" r="3.6"/><path d="M10 1.5v2.2M10 16.3v2.2M1.5 10h2.2M16.3 10h2.2M4 4l1.6 1.6M14.4 14.4 16 16M4 16l1.6-1.6M14.4 5.6 16 4"/></g><g class="ti-dark"><path d="M16.5 12.4A7 7 0 0 1 7.6 3.5a7 7 0 1 0 8.9 8.9z"/></g></svg>"""


def icon(slug, alt, size, lazy=True):
    light, dark = ICONS[slug]
    ld = ' loading="lazy"' if lazy else ''
    return (f'<span class="tool-icon"><img class="ic-light" src="{light}" width="{size}" height="{size}" alt="{alt}"{ld} decoding="async">'
            f'<img class="ic-dark" src="{dark}" width="{size}" height="{size}" alt=""{ld} decoding="async"></span>')


def url(lang, slug):
    return (UI[lang]["prefix"] + f"/{slug}/")


def page(slug, lang):
    u, c = UI[lang], P[slug][lang]
    n, idx = NAMES[slug], ORDER.index(slug) + 1
    other = u["other"]
    self_url, other_url = url(lang, slug), url(other, slug)
    mailto = f"mailto:{MAIL}?subject=" + c["subject"].replace(" ", "%20")
    nav_tools = "\n".join(
        f'      <a href="{url(lang, s)}"' + (' aria-current="page"' if s == slug else '') + f'>{NAMES[s]}</a>' for s in ORDER)
    status_cls, status_txt = c["status"]
    chips = "".join(f"<span>{p}</span>" for p in c["platforms"])
    why = "\n".join(f'        <article>\n          <h3>{h}</h3>\n          <p>{p}</p>\n        </article>' for h, p in c["why"])
    feats = "\n".join(f'        <article class="feature">\n          <h3>{h}</h3>\n          <p>{p}</p>\n        </article>' for h, p in c["features"])
    princ = "\n".join(f'          <li><b>{h}</b><p>{p}</p></li>' for h, p in u["principles"])
    spec = "\n".join(
        f'        <div><dt>{dt}</dt><dd>{dd}' + (f'<small>{sm}</small>' if sm else '') + '</dd></div>' for dt, dd, sm in c["spec"])
    team = []
    for s in ORDER:
        sc = P[s][lang]
        alt = u["icon_alt"].format(n=NAMES[s])
        here = f' <em>{u["here"]}</em>' if s == slug else ''
        inner = (f'{icon(s, alt, 64)}\n          <span class="meta">{sc["meta"]}{here}</span>\n'
                 f'          <b>{NAMES[s]}</b>\n          <p>{sc["short"]}</p>')
        if s == slug:
            team.append(f'        <div class="rt here" aria-current="page">\n          {inner}\n        </div>')
        else:
            team.append(f'        <a class="rt" href="{url(lang, s)}">\n          {inner}\n        </a>')
    team = "\n".join(team)
    rot = P[slug]["rot"]
    legal = ('<a href="/impressum.html">' + u["imprint"] + '</a>\n      <a href="/datenschutz.html">' + u["privacy"] + '</a>')
    other_attr = f'hreflang="{other}" lang="{other}"'

    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{c["title"]}</title>
<meta name="description" content="{c["desc"]}">
<link rel="canonical" href="{SITE}{self_url}">
<link rel="alternate" hreflang="de" href="{SITE}{url('de', slug)}">
<link rel="alternate" hreflang="en" href="{SITE}{url('en', slug)}">
<link rel="alternate" hreflang="x-default" href="{SITE}{url('de', slug)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{self_url}">
<meta property="og:title" content="{n} · Alpine Swift">
<meta property="og:description" content="{c["desc"]}">
<meta property="og:locale" content="{u["locale"]}">
<meta name="theme-color" content="#F4F1FC" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0A0420" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/archivo-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/onest-var.woff2" as="font" type="font/woff2" crossorigin>
<script>try{{var t=localStorage.getItem("theme");if(t==="light"||t==="dark")document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="stylesheet" href="/assets/css/site.css">
</head>
<body>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{u["home"]}" aria-label="{u["brand_label"]}">
      {MARK}
      <span>Alpine <em>Swift</em></span>
    </a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="{u["menu"]}">
      <svg viewBox="0 0 20 20" aria-hidden="true"><path d="M2 6h16M2 14h16" stroke="currentColor" stroke-width="1.8"/></svg>
    </button>
    <nav class="nav" id="nav" aria-label="{u["nav_label"]}">
      <a href="{u["home"]}">{u["studio"]}</a>
{nav_tools}
      <a class="lang" href="{other_url}" {other_attr}>{u["other_label"]}</a>
      <a class="btn primary" href="#{u["cid"]}">{u["interest"]}</a>
    </nav>
    <button class="theme-btn" type="button" data-theme-toggle data-mode="auto" aria-label="{u["theme_label"]}">{THEME_ICON}</button>
  </div>
</header>

<main id="top">
  <section class="p-hero" aria-labelledby="p-title">
    <div class="wrap">
      <div class="p-hero-text">
        <p class="label"><b>Alpine Swift</b> · {c["label"]}</p>
        <h1 id="p-title">{n}</h1>
        <p class="tagline">{c["tagline"]}</p>
        <p class="lede">{c["lede"]}</p>
        <div class="p-badges"><p class="status {status_cls}">{status_txt}</p><div class="chips">{chips}</div></div>
        <div class="hero-ctas">
          <a class="btn primary" href="#{u["cid"]}">{u["interest"]}</a>
          <a class="btn" href="#{u["fid"]}">{u["features"]}</a>
        </div>
      </div>
      <div class="p-map" aria-hidden="true">
        <svg viewBox="0 0 400 400" preserveAspectRatio="xMidYMid slice">
          <g transform="rotate({rot} 200 200)">
            <rect class="ring" x="-60" y="-50" width="530" height="505" rx="215"/>
            <rect class="ring idx" x="-12" y="-4" width="430" height="412" rx="180"/>
            <rect class="ring" x="30" y="34" width="346" height="334" rx="146"/>
            <rect class="ring" x="62" y="64" width="282" height="272" rx="120"/>
            <rect class="ring idx" x="88" y="90" width="228" height="222" rx="98"/>
            <rect class="ring" x="104" y="104" width="196" height="194" rx="84"/>
          </g>
          <path class="trailpath" d="{P[slug]["path"]}"/>
        </svg>
        {icon(slug, "", 256, lazy=False)}
        <span class="corner tl">{u["tools_of"].format(i=f"0{idx}")}</span>
        <span class="corner br">{c["corner"]}</span>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="why-title">
    <div class="wrap">
      <div class="sec-head">
        <p class="label">{u["why"].format(n=n)} <span class="rwr" aria-hidden="true"><i></i><i></i><i></i></span></p>
        <h2 id="why-title">{c["why_h"]}</h2>
        <p>{c["why_p"]}</p>
      </div>
      <div class="audience">
{why}
      </div>
    </div>
  </section>

  <section class="section" id="{u["fid"]}" aria-labelledby="feat-title" style="padding-top:0">
    <div class="wrap">
      <div class="sec-head">
        <p class="label">{u["features"]}</p>
        <h2 id="feat-title">{u["features_h"].format(n=n)}</h2>
      </div>
      <div class="features">
{feats}
      </div>
    </div>
  </section>

  <section class="section principles" aria-labelledby="pr-title">
    <div class="wrap">
      <div class="sec-head">
        <p class="label">{u["principles_label"]}</p>
        <h2 id="pr-title">{u["principles_h"]}</h2>
        <p>{c["assist"]}</p>
      </div>
      <ul class="principle-list" role="list">
{princ}
      </ul>
    </div>
  </section>

  <section class="section" aria-labelledby="spec-title">
    <div class="wrap">
      <div class="sec-head">
        <p class="label">{u["spec_label"]}</p>
        <h2 id="spec-title">{u["spec_h"].format(n=n)}</h2>
      </div>
      <dl class="spec">
{spec}
      </dl>
    </div>
  </section>

  <section class="section" aria-labelledby="team-title" style="padding-top:0">
    <div class="wrap">
      <div class="sec-head">
        <p class="label">{u["team_label"]}</p>
        <h2 id="team-title">{u["team_h"]}</h2>
        <p>{u["team_p"]}</p>
      </div>
      <div class="ropeteam">
{team}
      </div>
    </div>
  </section>

  <section class="section summit p-cta" id="{u["cid"]}" aria-labelledby="cta-title">
    <div class="wrap">
      <div class="summit-text">
        <p class="label"><b>{n}</b> · {u["cta_label"]} <span class="rwr" aria-hidden="true"><i></i><i></i><i></i></span></p>
        <h2 id="cta-title">{c["cta_h"]}</h2>
        <p>{c["cta_p"]}</p>
        <div class="mail">
          <a class="addr" href="{mailto}">{MAIL}</a>
          <button class="btn" type="button" data-copy="{MAIL}" data-done="{u["copied"]}"><span>{u["copy"]}</span></button>
        </div>
        <p class="back">{u["back"]}</p>
      </div>
      {icon(slug, "", 256)}
    </div>
  </section>
</main>

<footer class="site-footer">
  <div class="wrap">
    <span>© <span data-year>2026</span> Alpine Swift · Peter Hildel</span>
    <nav aria-label="{u["legal_label"]}">
      <a href="{u["home"]}">Alpine Swift</a>
      {legal}
      <a href="{other_url}" {other_attr}>{u["other_lang_name"]}</a>
    </nav>
  </div>
</footer>

<script src="/assets/js/site.js" defer></script>
</body>
</html>
"""


for slug in ORDER:
    for lang in ("de", "en"):
        out = os.path.join(ROOT, url(lang, slug).strip("/"), "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(page(slug, lang))
        print("wrote", out)
