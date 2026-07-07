# Sources — Revue de Presse Assurance PME (Layer 3 — Reference)

Compagnon de `persona.md`. Objectif : remplacer/compléter les sources actuelles (M&A grandes entreprises, finance institutionnelle, sport) par des sources alignées sur les critères de pertinence du persona.

---

## Diagnostic

Le problème n'est pas le volume (11 articles), c'est le créneau : les sources actuelles semblent être de la presse financière/business généraliste. Le persona cible un créneau étroit et spécifique (assurance de personnes pour dirigeants/travailleurs autonomes, régimes collectifs PME, régulation Québec, fragilité financière PME). Il faut des sources qui écrivent *nativement* dans ce créneau, pas des sources généralistes qu'on filtre après coup.

---

## Tier 1 — Presse spécialisée assurance (Québec/Canada) — PRIORITÉ

| Source | URL | Angle | Accès |
|---|---|---|---|
| Portail de l'assurance | portail-assurance.ca | Assurance de personnes ET dommages, marché québécois, couvre PME régulièrement | Infolettre quotidienne gratuite ; certains contenus premium |
| Journal de l'assurance | portail-assurance.ca/journal-assurance | Dossiers stratégiques, entrevues dirigeants, analyse de fond | Payant (magazine + web) |
| Insurance Journal (Insurance Portal) | insurance-portal.ca | Version anglophone du Portail — dommages, personnes, services financiers | Infolettre gratuite (tier de base) |
| Conseiller.ca — section Conseiller PME | conseiller.ca/conseiller-pme | Nouvelles PME, angle courtier/conseiller, très proche du persona | Gratuit |
| Insurance Business Canada | insurancebusinessmag.com/ca | Tendances marché, insurtech, mouvements industrie | Gratuit, infolettre |

**Note :** vérifier si "Avantages" (magazine régimes collectifs/PME) existe toujours sous ce nom avant de l'ajouter — je ne l'ai pas confirmé dans mes recherches récentes.

---

## Tier 2 — Régulation (Québec/Canada)

| Source | URL | Angle |
|---|---|---|
| AMF (Autorité des marchés financiers) | lautorite.qc.ca | Communiqués, service d'abonnement courriel dédié (E-mail Info) |
| Chambre de la sécurité financière (CSF) | chambresf.com | Organisme d'encadrement des conseillers en assurance de personnes au Québec — plus directement pertinent que CIRO pour ton créneau |
| Chambre de l'assurance de dommages (CHAD) | chad.ca | Pertinent pour le volet assurance des entreprises/PME |
| CIRO | ciro.ca | Mentionné dans ton persona — couvre plutôt les courtiers en placement/fonds, angle plus périphérique |

---

## Tier 3 — Presse PME / entrepreneuriat (angle risque financier)

| Source | URL | Angle |
|---|---|---|
| FCEI / CFIB | cfib-fcei.ca/research-economic-analysis | Rapport dédié "Insuring Main Street" (marché assurance PME), Baromètre des affaires mensuel, sondages réguliers — excellente source de statistiques citables |
| Les Affaires | lesaffaires.com | Section PME/entrepreneuriat Québec |
| BDC (Banque de développement du Canada) | bdc.ca | Articles et études sur la gestion des risques PME |
| Investment Executive / Advisor.ca | investmentexecutive.com, advisor.ca | Anglophone, angle courtiers/conseillers financiers |

---

## Tier 4 — Insurtech / Fintech (SME coverage)

| Source | URL | Angle |
|---|---|---|
| Insurance-Canada.ca | insurance-canada.ca | Blog dédié insurtech au Canada |
| Insurance Business Canada (section tech) | insurancebusinessmag.com/ca | Tendances insurtech/fintech affectant la couverture PME |

---

## Notes d'implémentation

1. **RSS manquant** : pour les sources sans flux RSS natif, générer un flux via un agrégateur tiers (Feedly, Inoreader) pointant vers l'URL de la section pertinente (ex. conseiller.ca/conseiller-pme).
2. **Infolettres** : plusieurs sources (Portail de l'assurance, AMF, Investment Executive) n'offrent qu'une infolettre par courriel — envisager un parsing d'email si le pipeline ne peut consommer que du RSS.
3. **Priorité de démarrage** : commencer par Portail de l'assurance + Conseiller PME + FCEI/CFIB — meilleur ratio pertinence/volume, et couvrent à eux trois la majorité des critères d'inclusion du persona (assurance PME, statistiques de fragilité, angle conseiller).
4. **Revalidation périodique** : les sources spécialisées assurance changent souvent de structure d'abonnement (paywall) — prévoir une vérification trimestrielle de l'accessibilité réelle des flux.
