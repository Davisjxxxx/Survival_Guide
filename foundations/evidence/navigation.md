# Navigation, weather observation and rescue · evidence pack

Checked 2026-11-24. Topographic map reading, compass/declination principles, weather recognition, lost-person decisions and emergency signaling in the United States. Use `N01–N10` alongside `T06`, `T08`, `T11`, `T14–T16` and `E01–E18` in the [claim register](claims.tsv).

| Decision | Source-supported boundary | Editorial implementation |
|---|---|---|
| Maps, symbols and scale | USGS topographic maps provide contours, scale, hydrography and date metadata (N01–N03); public-domain historical excerpts such as 1965 Ely 1:24,000 require credit and symbols-only disclaimers (N04). | Preserve the missing `B014 P01–P10` recovery requirement by using explicit `Z11-R01`..`Z11-R10` reconstruction IDs alongside adapted `B014 P11–P20` (`Z11-P11`..`Z11-P20`). |
| Compass, declination and interference | True, grid and magnetic north differ by local date-dependent declination (T08, N08); nearby metal, electronics and iron-rich rock deflect magnetic needles erratically (N08). | Reject nature-folklore direction myths; enforce metal-clearance checks and current declination lookup. |
| Weather, fog and water barriers | Visual cloud/front/pressure cues supplement official NWS forecasts and NOAA Weather Radio (N06, T14–T16); fog/whiteout collapses visual navigation (N07); flooded crossings and uncertain ice require land detours or staying put (N10, E12). | Tie every weather or visibility degradation cue directly to an objective turnaround or stay-put stop threshold. |
| Signaling, beacons and SAR coordination | Registered 406 MHz PLBs provide one-way distress alerts via NOAA SARSAT with clear sky view (N05); lost parties should stay put unless immediate danger requires movement, stay visible and report last known point clearly (N09, T06). | Keep lost-person stay/signal/move rules and group separation protocols consistent across Z01 and Z11. |

Independent cartography, search-and-rescue, meteorology and emergency-communications specialists must review declination diagrams, contour exercises, PLB/messenger limits and rescue protocols prior to field authorization.
