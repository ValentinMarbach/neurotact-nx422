# Contexte à donner à Claude — projet NX-422 NeuroTact, ma partie (LSE1)

## Instructions pour toi, Claude
Je suis étudiant en master à l'EPFL, dans le cours NX-422 Neural Interfaces. Je suis dans les transports et je veux **comprendre** ma partie du projet en discutant avec toi.
- Réponds en **français**, avec des messages **courts** (je lis sur mon téléphone). Pas de longs tableaux.
- Explique les mécanismes simplement. Pars de l'intuition, puis donne le chiffre.
- Quand je te le demande, **interroge-moi** : une question à la fois, puis corrige ma réponse.
- Base-toi sur les faits ci-dessous. Si tu ajoutes une connaissance générale qui n'y figure pas, dis-le. N'invente pas de chiffres.
- Aide-moi aussi à préparer les questions que le TA ou le jury pourraient poser (présentation le 10–11 déc. 2026, rapport le 18 déc.).

---

## 1. Le projet en bref
**NeuroTact** est un implant cortical qui **rend le toucher** à une main robotique ou prothétique pilotée par une **BCI motrice** (implant dans M1). Il **stimule électriquement** la zone de la main du cortex somatosensoriel primaire (**S1**, aire 1 et aire 3b superficielle) : c'est l'**ICMS** (intracortical microstimulation). Le patient ressent alors un toucher sur sa propre main. NeuroTact **enregistre** aussi la réponse corticale à chaque stimulation, ce qui permet une boucle fermée.

Les éléments du design actuel (résumé S6 du 9 oct. 2026) :
- **64 shanks** flexibles en polyimide, d'environ 10 µm × 50 µm de section et jusqu'à 4 mm de long, disposés en grille **8×8 au pas de 400 µm**.
- **4 sites par shank** de ~1000 µm², revêtus de **SIROF** (oxyde d'iridium pulvérisé), soit **256 sites** au total.
- Les shanks sont insérés inclinés vers la paroi postérieure du sillon central, pour atteindre l'aire 1 et l'aire 3b. Un raidisseur résorbable (soie ou PEG) aide à l'insertion.
- Un **ASIC** porte 64 générateurs de courant indépendants et une matrice de commutation 256 → 64. L'enregistrement se fait avec un *blanking* des artefacts.
- Un petit **réseau de neurones** sur la puce transforme les capteurs de force de la main en trains d'impulsions biomimétiques. Il est entraîné sur TouchSim.
- Un **algorithme de recalibration** ajuste le courant de chaque électrode quand son seuil dérive. Le plafond actuel est de **40 µA**.
- Tout est implanté : boîtier en titane, alimentation et données par un lien inductif à 13,56 MHz, budget de puissance < 15 mW.
- Les impulsions sont biphasiques, cathodiques en premier, 200 µs par phase, 50–300 Hz.

Le groupe compte 4 rôles : **EE** (électronique et puissance), **CS** (algorithmes), **LSE1** (moi : justification biologique et clinique) et **LSE2** (matériaux, fabrication, chirurgie).

**Ma partie (LSE1)** couvre 5 points :
1. la population cible ;
2. la dérive des seuils : ce que c'est, quel signal la détecte, pourquoi recalibrer malgré des sondes flexibles ;
3. le passage des seuils de la souris à l'humain ;
4. pourquoi 256 sites ;
5. les limites de sécurité tissulaire (densité de charge, Shannon) et leurs réserves pour l'humain.

---

## 2. Population cible
**Critique du TA :** les amputés pilotés par une BCI motrice sont rares. Les BCI humaines concernent surtout des tétraplégiques, et les amputés pilotent leur prothèse par EMG.

**Ce que disent les articles :**
- **Tous** les humains implantés avec une BCI motrice ou une ICMS sont **paralysés**, presque toujours après une lésion de la moelle cervicale (SCI C4–C6). **Aucun amputé.** Exemples : Collinger 2013, Flesher 2016/2021, Hughes 2021, Greenspon 2025 (3 patients), Armenta Salas 2018, Szymanski 2021.
- Les études ne portent que sur 1 ou 2 participants chacune (Greenspon 2025). Il y a de l'ordre de quelques dizaines d'implantés dans le monde (pas de source dans mon dossier).
- Les amputés utilisent des prothèses **myoélectriques** (EMG) ou à câble. Pour leur rendre le toucher, on stimule les **nerfs du moignon** (cuff, TIME, USEA). L'ICMS est réservée à ceux qui *« cannot benefit from an interface with the peripheral nervous system »* (Flesher 2016).
- Il y a environ **169 000 tétraplégiques par SCI aux États-Unis**, et près de la moitié placent la fonction de la main avant toute autre priorité (Flesher 2021). On compte plus de 20 millions d'amputés traumatiques du membre supérieur dans le monde, mais les amputations très proximales sont rares : désarticulation de l'épaule 3 %, interscapulo-thoracique 2 %.

**La carte de la main dans S1 tient-elle ?**
- **Après une amputation**, oui : elle reste stable jusqu'à 5 ans (r = 0,68–0,91, Schone 2025) et est préservée (Makin 2013).
- **Après une SCI**, elle est présente mais **se dégrade avec les années** (r_s = −0,59 entre les années depuis la lésion et la typicité de la carte, Kikkert 2021). Il faut donc **implanter tôt**.

**Bénéfice démontré :** avec le retour ICMS, une tâche de saisie passe de 20,9 s à 10,2 s (−51 %, Flesher 2021, 1 patient).

**Ma proposition :** cibler les **personnes qui pilotent un bras robotique ou prothétique avec une BCI intracorticale** (d'abord les SCI cervicales). Les **amputés** deviennent un sous-cas, limité à ceux **sans nerf utilisable** (épaule désarticulée, plexus brachial arraché). La BCI motrice est un système compagnon et ne fait pas partie de NeuroTact.

---

## 3. Dérive des seuils
**Le mécanisme :** le seuil de perception dépend de la **distance entre le site et les neurones excitables**. La réponse à corps étranger éloigne les neurones :
- de quelques minutes à 24 h : la microglie entoure l'implant ;
- dès la 1re semaine : les astrocytes s'activent ;
- après 6–8 semaines : une **gaine compacte de 50–100 µm** s'est formée, avec une perte de neurones et une fuite de la barrière hémato-encéphalique qui persiste tant qu'il y a un décalage mécanique (Polikov 2005, Kozai 2015).

S'y ajoute **l'usure de l'électrode** : sur des Utah humains explantés, 41 % des pointes stimulées sont abîmées contre 6 % des non stimulées, en lien avec la charge injectée sous −0,6 V (Woeppel 2021).
Exemple parlant (Lycke 2023) : une lésion accidentelle a fait passer un seuil de 4,45 à 13,73 µA, puis il est revenu à 4,87 µA en 116 jours.

**Ce que font vraiment les seuils (surprise) :**
- Sur un Utah humain, les seuils **baissent** : médiane de **31,5 µA à J100 → 10,4 µA à J1500**, surtout entre J100 et J500 (Hughes 2021). Ils restent très dispersés d'une électrode à l'autre, et **varient de plus de 10 µA d'un jour à l'autre**. Chaque jour, 50–60 électrodes sur 64 fonctionnent.
- Sur 6 mois, 5 électrodes sur 19 ont vu leur seuil **monter** (+0,35 µA/jour, Flesher 2016).
- Chez la souris avec une sonde ultraflexible, les seuils décroissent pendant **20–70 jours**, puis forment un plateau (variation ≤ 1 µA sur plus de 150 jours, Lycke 2023).

**Sondes flexibles :** elles donnent moins de cicatrice et une densité neuronale normale (Luan 2017, Lycke 2023). **Mais** leurs sondes font **1 µm** d'épaisseur et les nôtres **10 µm**. La rigidité varie comme l'épaisseur au cube, donc les nôtres sont ~1000× plus rigides (mon estimation). On ne peut donc pas promettre « zéro cicatrice ».

**Quel signal pour détecter la dérive ?** La **réponse évoquée** par une impulsion test, c'est-à-dire l'activité multi-unitaire ou le potentiel évoqué enregistrés sur les **sites voisins**. On peut l'enregistrer dès **~0,7 ms** après l'impulsion (singe, Sombeck 2022). Pour les artefacts, on utilise un *blanking* par échantillonneur-bloqueur de **1,6 ms** et on rejette les 2 premières ms (humain, Shelchkova 2023). L'impédance et la tension interphase servent en complément : elles renseignent sur l'électrode, pas sur le tissu.
**Limite :** aucun article ne montre que la réponse évoquée suit le **seuil perceptif**. Les retours occasionnels du patient servent donc à recaler l'échelle.

**Pourquoi recalibrer malgré tout, et quel gain par rapport aux Utah ?** Aujourd'hui, la calibration est manuelle et pénible : des sessions de 4 h, 3 fois par semaine, et seulement **4 cartes complètes des seuils en 1500 jours** (Hughes 2021). La boucle fermée apporte :
1. le suivi de la phase précoce ;
2. l'absorption de la variabilité au jour le jour, pour une intensité constante ;
3. des intensités homogènes entre sites, indispensables pour les motifs multi-électrodes ;
4. une stimulation près du seuil, donc moins de charge et moins d'usure.

**À ne pas promettre :** une durée de vie plus longue (les Utah tiennent déjà plus de 1500 jours).

---

## 4. Seuils : de la souris à l'humain
- **Lycke 2023** a travaillé sur 5 souris, avec des sites de 24 µm de diamètre (~450 µm²) et des impulsions de 167 µs à 100 Hz. Les seuils sont de **~2–7 µA**, et **1,5 µA (0,25 nC/phase)** suffit pendant plus de 8 mois. Ces seuils sont plus bas dans les couches L4–L6. Des sondes rigides demandent 15–30 µA chez la souris.
- **Lycke ne projette AUCUN seuil humain**, alors que le S6 l'affirme à tort.
- Chez le **singe**, le seuil est d'environ 30 µA (Kim 2015b). Chez l'**humain avec Utah**, il va de 15 à 88 µA, avec une **médiane de 34,9 µA** (Flesher 2016) ; la JND (plus petite différence perçue) est de ~13–15 µA. Il n'y a que ~7 niveaux d'intensité discriminables entre le seuil et 100 µA (Greenspon 2025).
- **Pourquoi l'humain diffère :**
  - le cortex humain est plus épais, donc moins dense en neurones par volume ; il faut ~1,5× plus de courant (mon estimation). La paroi postérieure du sillon central (3b) ne fait que 1,81 mm (Fischl 2000) ;
  - nos shanks sont plus épais, et le cerveau humain a des pulsations et des micromouvements plus grands ;
  - la loi courant–distance est **I = k·r²**, avec k ≈ 1292 µA/mm² (Stoney 1968) : doubler la distance aux neurones multiplie le courant par 4.
- **Mon estimation :** une médiane humaine de **~8–20 µA**, une plage de ~3–40 µA, et une queue à 40–60 µA.
- **Conséquences :**
  - le **plafond à 40 µA est trop serré**. Avec un seuil de 20 µA et 4 niveaux d'intensité, on monte à ~75 µA ;
  - je propose une plage **matérielle de 0 à 100 µA** et un **plafond logiciel fixé par la charge**. Les « 40 µA » deviennent le seuil au-delà duquel on bascule vers un autre site du même shank ;
  - **tension de compliance** (estimation pour l'EE) : la résistance d'accès d'un site de 1000 µm² est de ~70–140 kΩ, soit 7–14 V à 100 µA. Il faut donc une compliance d'**au moins ±12 V**.

---

## 5. Pourquoi 256 sites
- La **carte de la main** mesure **~15,5 mm** du pouce à l'auriculaire, avec ~5 mm entre les centres de deux doigts voisins (Martuzzi 2014, IRMf 7T). L'aire 3b est sur la paroi postérieure du sillon, l'aire 1 sur la crête du gyrus.
- **Utah humain (Pittsburgh) :** 2 matrices de 2,4 × 4 mm, 60 shanks de 1,5 mm chacune, mais **32 seulement câblées** par matrice, soit **64 électrodes** au total, toutes dans l'aire 1. **Pas de sensation au pouce ni aux bouts des doigts**, 25–58 % d'électrodes inutiles, et une couverture de seulement 7–20 % de la paume.
- **Rayon activé :** r = √(I/k), soit 124 µm à 20 µA, 176 µm à 40 µA et 278 µm à 100 µA. Jusqu'à ~40 µA, les shanks voisins (espacés de 400 µm) restent à peu près indépendants.
- **Arguments pour 256 sites :**
  1. **la profondeur** : on atteint l'aire 3b, l'aire principale du toucher, que l'Utah ne touche pas ;
  2. **la redondance** : on choisit le meilleur des 4 sites de chaque shank ;
  3. **les groupes d'électrodes localisent mieux** : la localisation fausse passe de 42 % avec 1 électrode à 7 % avec 4 électrodes (Greenspon 2025) ;
  4. **une densité 10× plus élevée** : 256 sites contre 64 électrodes.
- **Points faibles :**
  - le pas latéral reste de 400 µm, comme l'Utah, donc la résolution latérale n'est pas meilleure ;
  - **la surface couverte est petite** : 8×8 au pas de 400 µm ne fait que **2,8 mm**, soit environ **un doigt** sur 15 mm ;
  - seuls 64 sites peuvent stimuler en même temps.
- **Options en discussion :** (a) réorganiser en 4×16 shanks (~6 mm, ~2 doigts) ; (b) passer le pas à 800 µm ; (c) assumer une cible « bout du pouce et de l'index ».

---

## 6. Sécurité tissulaire
Les formules : Q = I × durée de phase ; D = Q / surface ; k de Shannon = log D + log Q (D en µC/cm², Q en µC).
Pour un site de 1000 µm² (10⁻⁵ cm²) et des phases de 200 µs :
- 20 µA → 4 nC, 0,4 mC/cm², k = 0,20
- 30 µA → 6 nC, 0,6 mC/cm², k = 0,56
- 40 µA → 8 nC, 0,8 mC/cm², k = 0,81
- 100 µA → 20 nC, 2,0 mC/cm², k = 1,60

Le calcul du S6 est juste. **Les réserves :**
- **Shannon ne vaut pas pour les micro-électrodes.** Son modèle a été ajusté sur des disques de 0,01–0,5 cm² posés à la surface du cortex du chat (7 h, 50 Hz). Son seuil prudent est k = 1,5 ; la valeur **1,85 vient de Cogan 2016**, pas de Shannon.
- Pour les micro-électrodes, c'est la **charge par phase** qui compte : le seuil de dommage est d'environ **4 nC/phase** (Cogan 2016). Nous le dépassons déjà à 30–40 µA. Ce seuil dépend aussi de la fréquence et du cycle de service. Le premier mécanisme de dommage serait l'hyperactivité neuronale.
- La **pratique humaine** va jusqu'à 100 µA × 200 µs = 20 nC/phase, avec 144 nC au total (Flesher 2016), sans dommage clair. **Mais** c'était sur des sites Utah de ~2000 µm², soit le **double** des nôtres : 50 µA chez nous équivalent à 100 µA sur Utah en densité.
- La capacité d'injection du SIROF (1–5 mC/cm²) a été mesurée **in vitro avec polarisation** ; elle est ~4× plus faible in vivo. Sans polarisation, on sature vers ~50 µA à 200 µs.
- **Recommandations matérielles**, indépendantes de l'algorithme :
  - un plafond de charge par site d'environ 10–12 nC/phase, et 20 nC en absolu ;
  - un cycle de service limité (15 s ON / 15 s OFF) ;
  - la surveillance de la tension : désactiver un site si E_mc < −0,6 V ou si la tension interphase < −1,5 V.

---

## 7. Phrases du S6 à corriger
- La cible « amputés avec BCI motrice » : à élargir.
- « Flexible-probe thresholds are projected below 30 µA [Lycke] » : faux, ce sont des seuils de souris.
- Le plafond à 40 µA est trop bas.
- « k < 1,85 [Shannon] » : la valeur est de Cogan 2016, Shannon ne s'applique pas ici, et il faut ajouter la limite de 4 nC/phase.
- « 8 nC bien sous les 20 nC humains » : ces 20 nC portaient sur des sites deux fois plus grands.
- Le Qinj de 1–5 mC/cm² est une valeur in vitro.
- « ×4 densité » : c'est vrai en profondeur seulement, et la surface couverte reste petite.

## 8. Petit glossaire
- **S1, aires 3b et 1** : cortex somatosensoriel primaire. 3b est le toucher « principal », enfoui dans le sillon central ; 1 est sur la crête du gyrus.
- **ICMS** : microstimulation intracorticale.
- **Seuil de détection** : le plus petit courant que le patient perçoit.
- **JND** : la plus petite différence de courant perçue.
- **Champ projeté** : la zone de peau où le patient ressent la stimulation d'une électrode.
- **SIROF** : oxyde d'iridium pulvérisé, un revêtement à forte capacité d'injection de charge.
- **Qinj** : la charge maximale injectable sans réaction électrochimique nocive.
- **E_mc** : le potentiel cathodique maximal de l'électrode ; on ne doit pas descendre sous −0,6 V.
- **Tension de compliance** : la tension maximale que le stimulateur peut fournir pour imposer le courant.
- **Réponse à corps étranger** : la réaction du tissu à l'implant (microglie, astrocytes, gaine gliale).
- **Utah array** : une matrice rigide en silicium de 10×10 aiguilles de 1,5 mm (Blackrock), la référence actuelle.

## 9. Questions que tu peux me poser pour m'entraîner
- Pourquoi la cible « amputés + BCI motrice » pose-t-elle problème, et que propose-t-on à la place ?
- Si les seuils des Utah baissent avec le temps, pourquoi a-t-on besoin d'une recalibration automatique ?
- Quel signal enregistré détecte la dérive, et comment gère-t-on l'artefact de stimulation ?
- Pourquoi les 1,5 µA de Lycke ne se transposent-ils pas à l'humain ? Cite trois raisons.
- Que donne I = k·r² à 40 µA, et qu'est-ce que cela implique pour le pas de 400 µm ?
- Pourquoi l'équation de Shannon n'est-elle pas le bon critère pour nos sites ?
- Quel est le point faible de la grille 8×8, et quelles options a-t-on ?
