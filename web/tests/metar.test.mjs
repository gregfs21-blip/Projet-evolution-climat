// Tests du contrôle qualité P11 (critères Q2, Q3 et Q5), sur des METAR réels relevés par la sonde du 18/11/2026.
// Lancement : npm test (Node ≥ 22, --experimental-strip-types).
import assert from "node:assert/strict";
import { test } from "node:test";

import {
  bodyTemperature,
  check,
  matchesRaw,
  parseCsv,
  remarkTemperature,
  snapshot,
  staleMinutes,
  stationIndex,
} from "../lib/metar.ts";

const NOW = new Date("2026-11-18T11:55:00Z");
const STATIONS = stationIndex([
  { id: "FYKT", icaoId: "FYKT", site: "Keetmanshoop Arpt", country: "NA", elev: 1064 },
  { id: "UEEE", icaoId: "UEEE", site: "Yakutsk Arpt", country: "RU", elev: 98 },
  { id: "CXRB", icaoId: "CXRB", site: "Resolute Bay", country: "CA", elev: 67 },
  { id: "LFBD", icaoId: "LFBD", site: "Bordeaux/Mérignac Arpt", country: "FR", elev: 49 },
  { id: "FAUP", icaoId: "FAUP", site: "Upington Arpt", country: "ZA", elev: 848 },
  { id: "XXXX", icaoId: "XXXX", site: "Station de test", country: "FR", elev: 0 },
]);

const HEADER = "raw_text,station_id,observation_time,latitude,longitude,temp_c,dewpoint_c,maintenance_indicator_on";
const row = (raw, id, time, lat, lon, t, d, maint = "") => ({
  raw_text: raw, station_id: id, observation_time: time, latitude: String(lat), longitude: String(lon),
  temp_c: String(t), dewpoint_c: d === null ? "" : String(d), maintenance_indicator_on: maint,
});
const R = {
  fykt: row("METAR FYKT 181100Z AUTO 36008KT //// // ////// 39/M02 Q1016", "FYKT", "2026-11-18T11:00:00Z", -26.54, 18.111, 39, -2),
  ueee: row("METAR UEEE 181130Z 32001MPS 1100 R23/P2000N BR NSC M38/M41 Q1026 R23/450171 NOSIG RMK QNH7", "UEEE", "2026-11-18T11:30:00Z", 62.093, 129.774, -38, -41),
  cxrb: row("METAR CXRB 181100Z AUTO 29009KT M29/M32 RMK AO1 0PAST HR SOG 13 3002 SLP088 P0004 T12941320", "CXRB", "2026-11-18T11:00:00Z", 74.716, -94.983, -29.4, -32),
  lfbd: row("METAR LFBD 181130Z 24008KT 9999 FEW030 17/11 Q1018 NOSIG", "LFBD", "2026-11-18T11:30:00Z", 44.83, -0.69, 17, 11),
  faup: row("METAR FAUP 181100Z 12002KT CAVOK 38/M02 Q1015 NOSIG", "FAUP", "2026-11-18T11:00:00Z", -28.399, 21.26, 38, -2),
};
const toCsv = (rows) =>
  [HEADER, ...rows.map((r) => HEADER.split(",").map((k) => (/[",]/.test(r[k]) ? `"${r[k].replaceAll('"', '""')}"` : r[k])).join(","))].join("\n");

test("groupes de température du METAR brut", () => {
  assert.deepEqual(bodyTemperature(R.fykt.raw_text), { temp: 39, dew: -2 });
  assert.deepEqual(bodyTemperature(R.ueee.raw_text), { temp: -38, dew: -41 }); // R23/P2000N et R23/450171 ignorés
  assert.deepEqual(remarkTemperature(R.cxrb.raw_text), { temp: -29.4, dew: -32 });
  assert.equal(remarkTemperature(R.fykt.raw_text), null);
  assert.deepEqual(bodyTemperature("METAR XXXX 181100Z 00000KT 9999 M01/ Q1020"), { temp: -1, dew: null });
});

test("Q3 : température identique au METAR brut, groupe T prioritaire", () => {
  assert.equal(matchesRaw(39, R.fykt.raw_text), true);
  assert.equal(matchesRaw(-29.4, R.cxrb.raw_text), true);
  assert.equal(matchesRaw(-29, R.cxrb.raw_text), false); // le groupe T (−29,4) fait foi
  assert.equal(matchesRaw(40, R.fykt.raw_text), false);
  assert.equal(matchesRaw(10, "METAR XXXX 181100Z 00000KT 9999 Q1020"), false); // pas de groupe température
});

test("Q2 : observations réelles acceptées", () => {
  for (const r of [R.fykt, R.ueee, R.cxrb, R.lfbd]) {
    const o = check(r, STATIONS, NOW);
    assert.equal(typeof o, "object", `${r.station_id} : ${o}`);
  }
  const o = check(R.fykt, STATIONS, NOW);
  assert.equal(o.ageMin, 55);
  assert.equal(o.name, "Keetmanshoop Arpt");
});

test("Q2 : chaque règle d'exclusion", () => {
  assert.equal(check({ ...R.fykt, temp_c: "" }, STATIONS, NOW), "sans température");
  assert.equal(check({ ...R.fykt, observation_time: "2026-11-18T09:50:00Z" }, STATIONS, NOW), "trop ancienne");
  assert.equal(typeof check({ ...R.fykt, observation_time: "2026-11-18T09:55:00Z" }, STATIONS, NOW), "object"); // 2 h pile
  const hot = row("METAR XXXX 181100Z 00000KT 61/10 Q1010", "XXXX", "2026-11-18T11:00:00Z", 0, 0, 61, 10);
  assert.equal(check(hot, STATIONS, NOW), "hors bornes");
  const cold = row("METAR XXXX 181100Z 00000KT M91/M95 Q1010", "XXXX", "2026-11-18T11:00:00Z", 0, 0, -91, -95);
  assert.equal(check(cold, STATIONS, NOW), "hors bornes");
  const dew = row("METAR XXXX 181100Z 00000KT 10/12 Q1010", "XXXX", "2026-11-18T11:00:00Z", 0, 0, 10, 12);
  assert.equal(check(dew, STATIONS, NOW), "point de rosée supérieur à la température");
  assert.equal(check({ ...R.lfbd, maintenance_indicator_on: "TRUE" }, STATIONS, NOW), "maintenance");
  assert.equal(check({ ...R.lfbd, raw_text: R.lfbd.raw_text + " $" }, STATIONS, NOW), "maintenance");
  assert.equal(check({ ...R.lfbd, temp_c: "18" }, STATIONS, NOW), "différente du METAR brut");
  assert.equal(check({ ...R.lfbd, station_id: "ZZZZ", raw_text: R.lfbd.raw_text.replace("LFBD", "ZZZZ") }, STATIONS, NOW), "station inconnue");
});

test("classement, repère local, doublons et CSV entre guillemets", () => {
  const older = { ...R.fykt, observation_time: "2026-11-18T10:00:00Z", raw_text: R.fykt.raw_text.replace("181100Z", "181000Z").replace("39/M02", "37/M02"), temp_c: "37" };
  const csv = "# préambule éventuel\n" + toCsv([older, R.fykt, R.ueee, R.cxrb, { ...R.lfbd, raw_text: R.lfbd.raw_text + ', "test"' }, R.faup]);
  const s = snapshot(csv, STATIONS, NOW, "Wed, 18 Nov 2026 11:54:14 GMT");
  assert.equal(s.total, 5); // FYKT compté une fois : la mesure la plus récente
  assert.equal(s.kept, 5);
  assert.deepEqual(s.hottest.map((o) => o.id), ["FYKT", "FAUP", "LFBD", "CXRB", "UEEE"]);
  assert.equal(s.hottest[0].temp, 39);
  assert.deepEqual(s.coldest.map((o) => o.id).slice(0, 2), ["UEEE", "CXRB"]);
  assert.equal(s.reference?.id, "LFBD");
  assert.equal(s.referenceExclusion, null);
});

test("repère exclu ou absent : la raison est publiée", () => {
  const s = snapshot(toCsv([R.fykt, { ...R.lfbd, temp_c: "18" }]), STATIONS, NOW);
  assert.equal(s.reference, null);
  assert.equal(s.referenceExclusion, "différente du METAR brut");
  assert.equal(s.excluded["différente du METAR brut"], 1);
  assert.equal(snapshot(toCsv([R.fykt]), STATIONS, NOW).referenceExclusion, "absente du fichier");
});

test("Q5 : format changé ou fichier vide → erreur, jamais un résultat silencieux", () => {
  assert.throws(() => snapshot("a,b\n1,2", STATIONS, NOW), /en-tête/);
  assert.throws(() => snapshot(HEADER + "\n", STATIONS, NOW), /aucune observation/);
});

test("Q5 : lecture trop ancienne signalée", () => {
  assert.equal(staleMinutes("2026-11-18T11:30:00Z", NOW), null);
  assert.equal(staleMinutes("2026-11-18T11:00:00Z", NOW), 55);
});

test("parseCsv : guillemets doublés et fins de ligne CRLF", () => {
  assert.deepEqual(parseCsv('a,"b ""c"", d"\r\n1,2\r\n'), [["a", 'b "c", d'], ["1", "2"]]);
});
