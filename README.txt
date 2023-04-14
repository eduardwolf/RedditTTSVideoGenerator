Tento projekt sloužil pro automatickou tvorbu videí z příspěvků na Redditu.

Program vytvoří celé video s Text-To-Speech dabingem od Microsoftu.

Program najde nejlepší Reddit.com posty z vybraného fóra z vybraného období a vytvoří z nich "scénář",
poté vytvoří náhledový obrázek (thumbnail) pro Youtube videa.
Ze scénáře se pak vygeneruje Text-To-Speech audio file.
Pomocí ChromeDriveru jsou také vytvořeny snímky obrazovky z reddit příspěvku a komentářů, které jsou pak použity ve videu.

Scénář a audio se poté propojí a vytvoří se video, které zahrnuje snímky obrazovky, vše načasované dle délky audia.

Je nutný přístup k API Microsoftu TTS a Redditu, backgroumd .jpg pro thumbnaily a pozadí pro video přes které se bude dávat content. Obě může být jen černé.

Jedno spuštění může vygenerovat více videí, dle nastavení.

Ukázka výsledku tohoto projektu na mém Youtube kanálu:
https://www.youtube.com/watch?v=XPKNYPdlDHA&ab_channel=TheRedditNomad
