#!/usr/bin/env python3
"""Build output/lois-reglementations-generated.json from cours-lois-reglementations-v1.md content."""
import json
import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "output", "lois-reglementations-generated.json")

CHAPTERS = {
  "chapters": [
    {
      "title": "Les bases de la fiscalité française",
      "description": "Comprendre l'impôt sur le revenu, qui paie, comment déclarer, et les notions clés (tranches, quotient familial, revenus imposables).",
      "order": 1,
      "lessons": [
        {
          "title": "Comprendre l'impôt sur le revenu",
          "description": "Introduction à l'impôt sur le revenu en France : comment ça marche, qui paie, comment déclarer.",
          "order": 1,
          "difficulty": "easy",
          "estimatedDuration": 12,
          "content": {
            "textBlocks": [
              {
                "title": "Page 1",
                "content": "**L'impôt sur le revenu, c'est quoi ?**\n\nC'est l'impôt que tu paies chaque année sur tes revenus (salaire, revenus fonciers, pensions...). En France, c'est un impôt **progressif** : plus tu gagnes, plus tu paies en pourcentage. C'est différent d'un impôt proportionnel où tout le monde paie le même pourcentage.\n\n**Qui paie ?** Tous les résidents fiscaux français. Tu es résident fiscal français si : tu as ton foyer fiscal en France, tu passes plus de 183 jours par an en France, ou tu exerces une activité professionnelle principale en France.",
                "highlight": False
              },
              {
                "title": "Page 2",
                "content": "**Comment ça marche concrètement ?**\n\nChaque année tu déclares tes revenus de l'année précédente. L'administration fiscale calcule combien tu dois payer selon un barème progressif. Il y a 5 tranches : jusqu'à 11 294€ : 0% ; de 11 295€ à 28 797€ : 11% ; de 28 798€ à 82 341€ : 30% ; de 82 342€ à 177 106€ : 41% ; au-delà de 177 106€ : 45%.\n\n**Le quotient familial :** Si tu as des enfants, tu bénéficies de \"parts\" supplémentaires qui réduisent ton impôt. 1 enfant = 0,5 part, 2 enfants = 1 part supplémentaire.\n\n**La règle d'or :** Déclare TOUS tes revenus. L'administration a accès à beaucoup d'informations. Si tu oublies quelque chose, tu risques des pénalités.",
                "highlight": False
              }
            ],
            "quizBlocks": [
              {
                "Question": "Qu'est-ce que l'impôt sur le revenu en France ?",
                "questionType": "multiple-choice",
                "options": ["Un impôt proportionnel (même pourcentage pour tous)", "Un impôt progressif (plus tu gagnes, plus tu paies en pourcentage)", "Un impôt fixe (même montant pour tous)", "Un impôt optionnel"],
                "correctAnswer": "Un impôt progressif (plus tu gagnes, plus tu paies en pourcentage)",
                "explanationcorrect": "Exactement ! C'est un impôt progressif avec 5 tranches. Plus tu gagnes, plus le taux d'imposition augmente. Les tranches vont de 0% à 45%.",
                "explanationfalse": "Attention ! L'impôt sur le revenu en France est progressif, pas proportionnel. Plus tu gagnes, plus le pourcentage d'imposition augmente. Il y a 5 tranches de 0% à 45%.",
                "points": 5
              },
              {
                "Question": "Tu es résident fiscal français si tu passes plus de 183 jours par an en France.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Absolument ! 183 jours par an en France = résident fiscal français. Tu dois déclarer TOUS tes revenus mondiaux en France.",
                "explanationfalse": "C'est vrai ! Le critère des 183 jours est l'un des critères pour être résident fiscal français. Les autres : foyer fiscal en France ou activité professionnelle principale en France.",
                "points": 5
              },
              {
                "Question": "Associe chaque tranche à son taux : A. Jusqu'à 11 294€ ; B. De 28 798€ à 82 341€ ; C. Au-delà de 177 106€.",
                "questionType": "matching",
                "options": ["A. Jusqu'à 11 294€", "1. 0%", "B. De 28 798€ à 82 341€", "2. 30%", "C. Au-delà de 177 106€", "3. 45%"],
                "correctAnswer": "A → 1 (0%), B → 2 (30%), C → 3 (45%)",
                "explanationcorrect": "Parfait ! Jusqu'à 11 294€ = 0%. De 28 798€ à 82 341€ = 30%. Au-delà de 177 106€ = 45%. Ces tranches s'appliquent progressivement.",
                "explanationfalse": "Revois les tranches : jusqu'à 11 294€ = 0% ; de 28 798€ à 82 341€ = 30% ; au-delà de 177 106€ = 45%. Il y a aussi 11% et 41% pour les tranches intermédiaires.",
                "points": 5
              },
              {
                "Question": "Qu'est-ce que le quotient familial ?",
                "questionType": "multiple-choice",
                "options": ["Le montant total de tes revenus", "Un système qui réduit ton impôt si tu as des enfants", "Le nombre de personnes dans ton foyer", "Le montant de ton impôt"],
                "correctAnswer": "Un système qui réduit ton impôt si tu as des enfants",
                "explanationcorrect": "Exactement ! Le quotient familial te donne des parts supplémentaires si tu as des enfants. Plus tu as d'enfants, plus ton impôt est divisé.",
                "explanationfalse": "Non ! Le quotient familial donne des \"parts\" supplémentaires si tu as des enfants (1 enfant = 0,5 part, 2 enfants = 1 part). Plus de parts = impôt réduit.",
                "points": 5
              },
              {
                "Question": "Tu dois déclarer tous tes revenus, même les petits montants.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Absolument ! Transparence totale = sécurité. Même 50€ d'intérêts, tout doit être déclaré. Les pénalités peuvent être lourdes.",
                "explanationfalse": "C'est vrai ! Tu dois déclarer TOUS tes revenus. L'administration croise les données. Si tu oublies quelque chose, tu risques des pénalités (10% du montant oublié minimum).",
                "points": 5
              },
              {
                "Question": "La déclaration des revenus se fait généralement en quelle période ?",
                "questionType": "multiple-choice",
                "options": ["Janvier", "Mai (pour les revenus de l'année précédente)", "Décembre", "Octobre"],
                "correctAnswer": "Mai (pour les revenus de l'année précédente)",
                "explanationcorrect": "Parfait ! La déclaration se fait généralement en mai (jusqu'au début juin selon ton département). Depuis 2019 c'est obligatoirement en ligne.",
                "explanationfalse": "Attention ! La déclaration se fait en mai (date selon ton département). Tu déclares les revenus de l'année précédente. Respecte les délais pour éviter les pénalités.",
                "points": 5
              }
            ]
          }
        },
        {
          "title": "Les revenus imposables et les abattements",
          "description": "Comprendre quels revenus sont imposables, quels abattements existent, et comment optimiser sa déclaration.",
          "order": 2,
          "difficulty": "easy",
          "estimatedDuration": 14,
          "content": {
            "textBlocks": [
              {
                "title": "Page 1",
                "content": "**Les différents types de revenus imposables :**\n\n1. **Revenus du travail :** Salaires, primes, indemnités, avantages en nature. Tout ce que tu reçois de ton employeur est imposable, sauf certaines exceptions (remboursements de frais, tickets restaurant dans la limite).\n\n2. **Revenus fonciers :** Si tu loues un bien, les loyers sont imposables. Tu peux déduire des charges (intérêts d'emprunt, travaux, assurance...).\n\n3. **Revenus de capitaux mobiliers :** Intérêts, dividendes. Soumis au PFU de 30% (12,8% impôt + 17,2% prélèvements sociaux), sauf si tu choisis le barème progressif.\n\n4. **Plus-values :** Vente d'un bien avec un gain. Imposable selon le type de bien et la durée de détention.",
                "highlight": False
              },
              {
                "title": "Page 2",
                "content": "**Les abattements** réduisent tes revenus imposables (avant calcul de l'impôt). Exemples : abattement 10% minimum sur les salaires ; abattement sur les revenus fonciers ; abattement sur les plus-values immobilières (6% par an après 5 ans, exonération après 22 ans).\n\n**Les réductions et crédits d'impôt** réduisent directement ton impôt : dons aux associations (66%), services à la personne (50%), investissement locatif (Pinel, Malraux...).\n\n**La règle d'or :** Connais tes droits ! Beaucoup paient trop d'impôts par méconnaissance des abattements et crédits d'impôt. Informe-toi, consulte un expert-comptable si besoin.",
                "highlight": False
              }
            ],
            "quizBlocks": [
              {
                "Question": "Quels revenus sont généralement imposables ?",
                "questionType": "multiple-choice",
                "options": ["Seulement les salaires", "Salaires, revenus fonciers, revenus de capitaux, plus-values", "Seulement les revenus supérieurs à 50 000€", "Aucun revenu n'est imposable"],
                "correctAnswer": "Salaires, revenus fonciers, revenus de capitaux, plus-values",
                "explanationcorrect": "Exactement ! Presque tout est imposable. Il existe des abattements et crédits d'impôt pour réduire ton impôt. Connais tes droits !",
                "explanationfalse": "Non ! Presque tous les revenus sont imposables : salaires, revenus fonciers, revenus de capitaux, plus-values. Il y a des exceptions et abattements, mais en général si tu gagnes de l'argent c'est imposable.",
                "points": 5
              },
              {
                "Question": "Les abattements réduisent directement le montant de ton impôt.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Faux",
                "explanationcorrect": "Absolument ! Les abattements réduisent tes revenus imposables (avant le calcul de l'impôt). Les réductions et crédits d'impôt, eux, réduisent directement l'impôt. Nuance importante !",
                "explanationfalse": "C'est faux ! Les abattements réduisent tes revenus imposables, pas directement ton impôt. Exemple : 10% sur 50 000€ = 45 000€ imposables. Les crédits d'impôt réduisent directement l'impôt.",
                "points": 5
              },
              {
                "Question": "Associe : A. Salaires ; B. Loyers (revenus fonciers) ; C. Intérêts (Livret A).",
                "questionType": "matching",
                "options": ["A. Salaires", "1. Imposables avec abattement 10% minimum", "B. Loyers", "2. Imposables avec déduction des charges", "C. Intérêts", "3. PFU 30% ou barème progressif"],
                "correctAnswer": "A → 1, B → 2, C → 3",
                "explanationcorrect": "Parfait ! Salaires = abattement 10%. Loyers = déduction des charges. Intérêts = PFU ou barème. Chaque type a son traitement.",
                "explanationfalse": "Revois : salaires = abattement 10% (ou frais réels). Loyers = déduction des charges. Intérêts = PFU 30% ou barème progressif au choix.",
                "points": 5
              },
              {
                "Question": "Qu'est-ce qu'un crédit d'impôt ?",
                "questionType": "multiple-choice",
                "options": ["Un prêt de l'État", "Une réduction directe de ton impôt", "Une augmentation de tes revenus", "Un abattement sur tes revenus"],
                "correctAnswer": "Une réduction directe de ton impôt",
                "explanationcorrect": "Exactement ! Crédit d'impôt = réduction directe de l'impôt. Si le crédit est supérieur à ton impôt, l'État te rembourse. Exemples : dons 66%, services à la personne 50%.",
                "explanationfalse": "Non ! Un crédit d'impôt réduit directement ton impôt final. Si tu dois 2000€ et as 500€ de crédit, tu paies 1500€. Plus avantageux qu'un abattement.",
                "points": 5
              },
              {
                "Question": "Les revenus de capitaux (intérêts, dividendes) sont généralement soumis au PFU de 30%.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Parfait ! PFU = Prélèvement Forfaitaire Unique de 30% (12,8% impôt + 17,2% prélèvements). Tu peux choisir le barème progressif si c'est plus avantageux.",
                "explanationfalse": "C'est vrai ! Le PFU de 30% s'applique sur intérêts et dividendes, sauf si tu optes pour le barème progressif. Compare les deux pour optimiser.",
                "points": 5
              },
              {
                "Question": "Les abattements sur les plus-values immobilières augmentent avec la durée de détention.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Absolument ! Après 5 ans : 6% d'abattement par an. Après 22 ans : exonération totale. La patience est récompensée fiscalement.",
                "explanationfalse": "C'est vrai ! Plus tu gardes longtemps, plus l'abattement est important. Après 5 ans : 6% par an. Après 22 ans : exonération totale.",
                "points": 5
              }
            ]
          }
        },
        {
          "title": "La déclaration en pratique",
          "description": "Délais, déclaration en ligne, et démarches concrètes pour déclarer tes revenus.",
          "order": 3,
          "difficulty": "easy",
          "estimatedDuration": 10,
          "content": {
            "textBlocks": [
              {
                "title": "Page 1",
                "content": "**Déclaration en ligne :** Depuis 2019 la déclaration est obligatoirement en ligne (sauf exceptions). Tu reçois ta réponse plus vite. Tu as jusqu'au début juin pour déclarer (date exacte selon ton département).\n\n**Ce qu'il faut déclarer :** Salaires (ton employeur transmet déjà les infos), revenus fonciers, revenus de capitaux, plus-values, pensions... Presque tout. Certains revenus sont pré-remplis, vérifie quand même.",
                "highlight": False
              },
              {
                "title": "Page 2",
                "content": "**Les erreurs fréquentes :** Oublier des revenus (même petits), ne pas mettre à jour ton adresse, oublier un changement de situation (mariage, naissance). Chaque oubli peut coûter des pénalités.\n\n**La règle d'or :** Déclare tout, vérifie les pré-remplis, et respecte les délais. En cas de doute, consulte impots.gouv.fr ou un professionnel.",
                "highlight": False
              }
            ],
            "quizBlocks": [
              {
                "Question": "La déclaration des revenus est obligatoirement en ligne depuis 2019.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Exactement ! Sauf exceptions, la déclaration se fait en ligne. C'est plus simple et tu reçois ta réponse plus vite.",
                "explanationfalse": "C'est vrai ! Depuis 2019 c'est obligatoirement en ligne. Tu as jusqu'au début juin selon ton département.",
                "points": 5
              },
              {
                "Question": "Tu dois déclarer uniquement les revenus que ton employeur n'a pas déjà transmis.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Faux",
                "explanationcorrect": "Tu dois déclarer TOUS tes revenus. Même si certains sont pré-remplis (salaires), tu dois vérifier et ajouter les autres (loyers, intérêts, etc.).",
                "explanationfalse": "Faux ! Tu dois déclarer tous tes revenus. Les infos employeur sont souvent pré-remplies mais tu dois compléter (revenus fonciers, capitaux, plus-values...) et vérifier.",
                "points": 5
              },
              {
                "Question": "Quelle est la période habituelle de déclaration des revenus ?",
                "questionType": "multiple-choice",
                "options": ["Janvier-février", "Mai-début juin", "Septembre-octobre", "Décembre"],
                "correctAnswer": "Mai-début juin",
                "explanationcorrect": "Parfait ! La déclaration se fait en mai (jusqu'au début juin selon ton département) pour les revenus de l'année précédente.",
                "explanationfalse": "Attention ! C'est en mai (date exacte selon ton département), pas en janvier ni en décembre. Tu déclares les revenus de l'année précédente.",
                "points": 5
              },
              {
                "Question": "Oublier de déclarer un petit revenu peut entraîner des pénalités.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Absolument ! Même un petit oubli peut coûter des pénalités (10% du montant oublié minimum). L'administration croise les données. Mieux vaut tout déclarer.",
                "explanationfalse": "C'est vrai ! Les pénalités s'appliquent même sur les petits montants. L'administration a accès à beaucoup d'informations. Transparence totale = sécurité.",
                "points": 5
              },
              {
                "Question": "Où peut-on faire sa déclaration en ligne ?",
                "questionType": "multiple-choice",
                "options": ["Uniquement en bureau des impôts", "Sur impots.gouv.fr (espace personnel)", "Uniquement par courrier", "Sur les réseaux sociaux"],
                "correctAnswer": "Sur impots.gouv.fr (espace personnel)",
                "explanationcorrect": "Exactement ! Tu te connectes sur impots.gouv.fr avec ton espace personnel. La déclaration est sécurisée et souvent pré-remplie.",
                "explanationfalse": "Non ! La déclaration se fait sur impots.gouv.fr, dans ton espace personnel. C'est obligatoire en ligne depuis 2019 (sauf exceptions).",
                "points": 5
              },
              {
                "Question": "Associe : A. Déclaration en ligne ; B. Revenus pré-remplis ; C. Délai de déclaration.",
                "questionType": "matching",
                "options": ["A. Déclaration en ligne", "1. Obligatoire depuis 2019", "B. Revenus pré-remplis", "2. À vérifier et compléter", "C. Délai", "3. Mai-début juin"],
                "correctAnswer": "A → 1, B → 2, C → 3",
                "explanationcorrect": "Parfait ! En ligne = obligatoire. Pré-remplis = à vérifier. Délai = mai-début juin. Toujours vérifier et compléter sa déclaration.",
                "explanationfalse": "Revois : déclaration en ligne obligatoire ; pré-remplis à vérifier et compléter ; délai mai-début juin selon département.",
                "points": 5
              }
            ]
          }
        },
        {
          "title": "Le quotient familial et les parts",
          "description": "Comprendre comment les parts fiscales et le quotient familial réduisent ton impôt.",
          "order": 4,
          "difficulty": "easy",
          "estimatedDuration": 11,
          "content": {
            "textBlocks": [
              {
                "title": "Page 1",
                "content": "**Le quotient familial** divise ton revenu imposable par un nombre de \"parts\". Plus tu as de parts, plus ton impôt est réduit.\n\n**Comment obtenir des parts ?** Tu as 1 part pour une personne seule. 1 part pour un couple marié/pacsé. Chaque enfant compte : 1er enfant = 0,5 part, 2e = 0,5 part, 3e = 1 part, 4e et plus = 1 part chacun. Certaines situations (invalidité, ancien combattant...) donnent des demi-parts en plus.",
                "highlight": False
              },
              {
                "title": "Page 2",
                "content": "**Exemple simple :** Tu dois 2000€ d'impôt et tu es seul (1 part). Si tu as 2 enfants (1 part en plus = 2 parts au total), ton impôt est calculé comme si tu avais deux \"moitiés\" de foyer : le plafonnement du quotient familial peut limiter l'avantage, mais en pratique les familles paient moins d'impôt par part que les célibataires.\n\n**La règle d'or :** Toute naissance, adoption ou changement de situation doit être déclaré pour mettre à jour tes parts et éviter des erreurs.",
                "highlight": False
              }
            ],
            "quizBlocks": [
              {
                "Question": "Le quotient familial réduit l'impôt des familles avec enfants.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Exactement ! Les enfants donnent des parts supplémentaires (0,5 ou 1 part). Plus de parts = impôt réparti sur plus de parts = impôt réduit pour les familles.",
                "explanationfalse": "C'est vrai ! Le quotient familial donne des parts supplémentaires aux familles (1 enfant = 0,5 part, 2e = 0,5, 3e = 1 part...). Ça réduit l'impôt.",
                "points": 5
              },
              {
                "Question": "Combien de parts supplémentaires pour le premier enfant ?",
                "questionType": "multiple-choice",
                "options": ["0 part", "0,5 part", "1 part", "2 parts"],
                "correctAnswer": "0,5 part",
                "explanationcorrect": "Parfait ! 1er enfant = 0,5 part, 2e = 0,5 part, 3e = 1 part, 4e et plus = 1 part chacun. Le couple a 2 parts de base.",
                "explanationfalse": "Attention ! Le premier enfant donne 0,5 part supplémentaire. Le deuxième aussi 0,5. À partir du 3e c'est 1 part par enfant.",
                "points": 5
              },
              {
                "Question": "Un couple sans enfant a combien de parts ?",
                "questionType": "multiple-choice",
                "options": ["1 part", "2 parts", "0,5 part", "3 parts"],
                "correctAnswer": "2 parts",
                "explanationcorrect": "Exactement ! Un couple (marié ou pacsé) a 2 parts. Une personne seule a 1 part. Les enfants ajoutent 0,5 ou 1 part selon le rang.",
                "explanationfalse": "Non ! Un couple a 2 parts. Une personne seule a 1 part. Les parts servent à diviser le revenus imposable pour le calcul de l'impôt.",
                "points": 5
              },
              {
                "Question": "Il faut déclarer une naissance pour bénéficier des parts supplémentaires.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Absolument ! Tout changement de situation (naissances, mariage, Pacs...) doit être déclaré pour mettre à jour ton quotient familial et payer le bon montant.",
                "explanationfalse": "C'est vrai ! Une naissance donne droit à des parts supplémentaires mais il faut la déclarer aux impôts pour que le calcul soit mis à jour.",
                "points": 5
              },
              {
                "Question": "Associe : A. 1 part ; B. 2 parts ; C. 0,5 part en plus.",
                "questionType": "matching",
                "options": ["A. 1 part", "1. Personne seule", "B. 2 parts", "2. Couple sans enfant", "C. 0,5 part en plus", "3. Premier ou deuxième enfant"],
                "correctAnswer": "A → 1, B → 2, C → 3",
                "explanationcorrect": "Parfait ! Personne seule = 1 part. Couple = 2 parts. Premier et deuxième enfant = 0,5 part chacun.",
                "explanationfalse": "Revois : 1 part = personne seule ; 2 parts = couple ; 0,5 part en plus = 1er ou 2e enfant.",
                "points": 5
              },
              {
                "Question": "Plus on a de parts, plus on paie d'impôt.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Faux",
                "explanationcorrect": "Faux ! Plus tu as de parts (enfants...), plus ton revenu est \"divisé\" pour le calcul, ce qui réduit généralement l'impôt. C'est un avantage pour les familles.",
                "explanationfalse": "C'est faux ! Plus de parts = avantage fiscal. Le revenu est réparti sur plus de parts, ce qui réduit l'impôt. Les familles en bénéficient.",
                "points": 5
              }
            ]
          }
        },
        {
          "title": "Déclarer : les pièges à éviter",
          "description": "Les erreurs courantes et les bonnes pratiques pour une déclaration sereine.",
          "order": 5,
          "difficulty": "easy",
          "estimatedDuration": 10,
          "content": {
            "textBlocks": [
              {
                "title": "Page 1",
                "content": "**Les pièges courants :** Oublier des revenus (même petits : intérêts d'un livret, rémunération d'un petit job). Ne pas mettre à jour ton adresse (tu peux rater des courriers). Oublier de déclarer un changement (mariage, naissance, divorce). Erreur de report (un chiffre mal recopié).\n\n**Les conséquences :** Pénalités de 10% minimum sur les montants oubliés, intérêts de retard, et en cas de mauvaise foi des sanctions plus lourdes.",
                "highlight": False
              },
              {
                "title": "Page 2",
                "content": "**Les bonnes pratiques :** Garde tes justificatifs (bulletins de salaire, attestations, relevés). Vérifie les pré-remplis (les employeurs et banques transmettent des infos, mais des erreurs sont possibles). Déclare dans les délais. En cas de doute, appelle le 0809 401 401 (service des impôts) ou consulte impots.gouv.fr.\n\n**La règle d'or :** Transparence et délais. Déclare tout, déclare à temps, et corrige une erreur dès que tu t'en rends compte (une procédure de correction existe).",
                "highlight": False
              }
            ],
            "quizBlocks": [
              {
                "Question": "Oublier de déclarer un petit revenu peut entraîner des pénalités.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Absolument ! Les pénalités s'appliquent même sur les petits montants (10% minimum). L'administration croise les données. Mieux vaut tout déclarer.",
                "explanationfalse": "C'est vrai ! Même 50€ d'intérêts oubliés peuvent déclencher des pénalités. La règle : déclare tout, même si ça te semble négligeable.",
                "points": 5
              },
              {
                "Question": "Les revenus pré-remplis par l'administration sont toujours corrects, inutile de vérifier.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Faux",
                "explanationcorrect": "Tu dois toujours vérifier ! Les employeurs et banques transmettent des infos mais des erreurs ou oublis sont possibles. Complète et corrige si besoin.",
                "explanationfalse": "Faux ! Il faut vérifier les pré-remplis et compléter ce qui manque (revenus non transmis, changements de situation). Des erreurs sont possibles.",
                "points": 5
              },
              {
                "Question": "En cas d'erreur sur ma déclaration, je peux la corriger.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Oui ! Une procédure de correction existe. Mieux vaut corriger dès que tu t'en rends compte. Consulte impots.gouv.fr ou contacte ton centre des impôts.",
                "explanationfalse": "C'est vrai ! Tu peux demander une correction. Plus tu t'y prends tôt, mieux c'est. Ne laisse pas traîner une erreur.",
                "points": 5
              },
              {
                "Question": "Quelle sanction minimum en cas de revenus oubliés ?",
                "questionType": "multiple-choice",
                "options": ["Aucune", "5% du montant oublié", "10% du montant oublié", "Amende fixe de 100€"],
                "correctAnswer": "10% du montant oublié",
                "explanationcorrect": "Exactement ! Les pénalités sont au minimum 10% du montant oublié. Elles peuvent être plus lourdes en cas de mauvaise foi. Mieux vaut tout déclarer.",
                "explanationfalse": "Attention ! Les pénalités sont au minimum 10% du montant non déclaré. Il peut s'ajouter des intérêts de retard. La transparence paie.",
                "points": 5
              },
              {
                "Question": "Je dois déclarer un changement de situation (mariage, naissance) aux impôts.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Absolument ! Mariage, naissance, Pacs, divorce... impactent ton quotient familial et ton impôt. Déclare tout changement pour payer le bon montant.",
                "explanationfalse": "C'est vrai ! Tout changement (mariage, naissance, etc.) doit être déclaré pour mettre à jour ta situation fiscale et éviter des erreurs de calcul.",
                "points": 5
              },
              {
                "Question": "Associe : A. Pré-remplis ; B. Pénalités ; C. Correction.",
                "questionType": "matching",
                "options": ["A. Pré-remplis", "1. À vérifier et compléter", "B. Pénalités", "2. Au moins 10% si oubli", "C. Correction", "3. Possible en cas d'erreur"],
                "correctAnswer": "A → 1, B → 2, C → 3",
                "explanationcorrect": "Parfait ! Pré-remplis = à vérifier. Pénalités = 10% minimum si oubli. Correction = possible. Bonnes pratiques = vérifier, déclarer tout, corriger si besoin.",
                "explanationfalse": "Revois : pré-remplis à vérifier ; pénalités 10% minimum sur les oublis ; une procédure de correction existe en cas d'erreur.",
                "points": 5
              }
            ]
          }
        }
      ]
    },
    {
      "title": "Fiscalité des placements et investissements",
      "description": "Comprendre comment sont imposés les produits d'épargne (Livret A, PEA, assurance-vie) et comment optimiser sa fiscalité légalement.",
      "order": 2,
      "lessons": [
        {
          "title": "Fiscalité des produits d'épargne et placements",
          "description": "Comprendre comment sont imposés les différents produits d'épargne (Livret A, PEA, assurance-vie, compte-titres).",
          "order": 1,
          "difficulty": "medium",
          "estimatedDuration": 14,
          "content": {
            "textBlocks": [
              {
                "title": "Page 1",
                "content": "**Produits défiscalisés :** Le **Livret A**, le LDDS, le LEP sont totalement exonérés d'impôts et de prélèvements sociaux. Tu ne déclares même pas les intérêts. Plafonds limités (22 950€ Livret A, 12 000€ LDDS...).\n\n**Compte d'épargne classique :** Les intérêts sont imposables. Tu choisis entre le **PFU à 30%** (12,8% impôt + 17,2% prélèvements sociaux) ou le **barème progressif** (intégration dans tes revenus).",
                "highlight": False
              },
              {
                "title": "Page 2",
                "content": "**Assurance-vie :** Avant 8 ans = PFU 30% sur les gains. Après 8 ans = abattement 4 600€ (9 200€ pour un couple) puis avantages. Après 8 ans et plus de 150 000€ = PFU 7,5% sur les gains. Plus tu gardes longtemps, plus c'est avantageux.\n\n**PEA (Plan d'Épargne en Actions) :** Après 5 ans, les plus-values sont **exonérées d'impôts** (mais pas des prélèvements sociaux 17,2%). Avant 5 ans = imposable. C'est le placement star pour investir en actions avec avantage fiscal.\n\n**Compte-titres :** Plus-values imposables (PFU 30% ou barème). Pas d'avantage fiscal, mais plus de flexibilité (pas de plafond, pas de durée minimale).",
                "highlight": False
              },
              {
                "title": "Page 3",
                "content": "**Les prélèvements sociaux** (17,2%) financent la sécurité sociale. Ils s'ajoutent à l'impôt sur la plupart des revenus de capitaux et plus-values. Même exonéré d'impôts (ex. PEA après 5 ans), tu paies quand même les 17,2%.\n\n**La règle d'or :** Choisis selon ton horizon. Court terme (précaution) = Livret A. Moyen/long terme = PEA (actions, avantage après 5 ans) ou assurance-vie (avantage après 8 ans).",
                "highlight": False
              }
            ],
            "quizBlocks": [
              {
                "Question": "Les intérêts du Livret A sont-ils imposables ?",
                "questionType": "multiple-choice",
                "options": ["Oui, toujours", "Non, ils sont totalement exonérés", "Oui, mais seulement au-delà d'un certain montant", "Ça dépend de ta tranche"],
                "correctAnswer": "Non, ils sont totalement exonérés",
                "explanationcorrect": "Exactement ! Livret A = exonération totale. Pas d'impôt, pas de prélèvements, pas de déclaration. Plafond 22 950€.",
                "explanationfalse": "Non ! Les intérêts du Livret A (et LDDS, LEP) sont totalement exonérés. Tu ne les déclares même pas. Plafond limité à 22 950€.",
                "points": 5
              },
              {
                "Question": "Le PEA offre une exonération d'impôts sur les plus-values après 5 ans.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Absolument ! Après 5 ans : exonération d'impôts sur les plus-values. Tu paies seulement les prélèvements sociaux (17,2%). Avant 5 ans c'est imposable.",
                "explanationfalse": "C'est vrai ! PEA après 5 ans = plus-values exonérées d'impôts. Tu paies quand même 17,2% de prélèvements sociaux. C'est LE placement pour investir en actions avec avantage fiscal.",
                "points": 5
              },
              {
                "Question": "Associe : A. Livret A ; B. PEA après 5 ans ; C. Compte-titres.",
                "questionType": "matching",
                "options": ["A. Livret A", "1. Exonération totale", "B. PEA après 5 ans", "2. Exonération impôts, prélèvements 17,2%", "C. Compte-titres", "3. PFU 30% ou barème"],
                "correctAnswer": "A → 1, B → 2, C → 3",
                "explanationcorrect": "Parfait ! Livret A = exonération totale. PEA après 5 ans = exonération impôts seulement. Compte-titres = pas d'avantage fiscal.",
                "explanationfalse": "Revois : Livret A = exonération totale ; PEA après 5 ans = exonération impôts (17,2% prélèvements restent) ; compte-titres = PFU ou barème.",
                "points": 5
              },
              {
                "Question": "Que sont les prélèvements sociaux ?",
                "questionType": "multiple-choice",
                "options": ["Un type d'impôt sur le revenu", "Des contributions qui financent la sécurité sociale (17,2%)", "Des frais bancaires", "Des taxes locales"],
                "correctAnswer": "Des contributions qui financent la sécurité sociale (17,2%)",
                "explanationcorrect": "Exactement ! 17,2% qui financent la sécu. Ils s'ajoutent à l'impôt sur les revenus de capitaux et plus-values. Même exonéré d'impôts (PEA 5 ans), tu les paies.",
                "explanationfalse": "Non ! Les prélèvements sociaux (17,2%) financent la sécurité sociale. Ils s'ajoutent à l'impôt sur la plupart des revenus de capitaux et plus-values.",
                "points": 5
              },
              {
                "Question": "L'assurance-vie offre un abattement de 4 600€ (9 200€ couple) après 8 ans.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Parfait ! Après 8 ans tu bénéficies d'un abattement sur les gains. Plus tu gardes longtemps, plus l'assurance-vie est avantageuse fiscalement.",
                "explanationfalse": "C'est vrai ! Après 8 ans : abattement 4 600€ (9 200€ pour un couple) sur les gains. Puis PFU 7,5% après 8 ans dans certains cas. La patience paie.",
                "points": 5
              },
              {
                "Question": "Tu peux choisir entre PFU 30% et barème progressif pour la plupart des revenus de capitaux.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Absolument ! Pour intérêts, dividendes, plus-values compte-titres tu as le choix. Compare selon ta tranche : PFU souvent avantageux si tranche élevée, barème si tranche faible.",
                "explanationfalse": "C'est vrai ! Tu as le choix entre PFU 30% et barème progressif. Le PFU est souvent mieux si tu es en tranche élevée (30%+). Compare les deux.",
                "points": 5
              },
              {
                "Question": "Pour l'épargne de précaution (court terme), quel placement privilégier ?",
                "questionType": "multiple-choice",
                "options": ["Compte-titres", "PEA", "Livret A (défiscalisé)", "Assurance-vie"],
                "correctAnswer": "Livret A (défiscalisé)",
                "explanationcorrect": "Exactement ! Pour le court terme et la précaution, le Livret A est idéal : exonération totale, disponible, plafond 22 950€.",
                "explanationfalse": "Pour la précaution (court terme) le Livret A est le plus adapté : défiscalisé, disponible. PEA et assurance-vie sont pour le moyen/long terme.",
                "points": 5
              }
            ]
          }
        },
        {
          "title": "Optimiser sa fiscalité : les stratégies légales",
          "description": "Découvrir les stratégies légales pour optimiser sa fiscalité sans fraude.",
          "order": 2,
          "difficulty": "medium",
          "estimatedDuration": 12,
          "content": {
            "textBlocks": [
              {
                "title": "Page 1",
                "content": "**Optimiser, c'est légal.** Utiliser les dispositifs légaux pour réduire son impôt (PEA, assurance-vie, réductions d'impôt) = optimisation. Cacher des revenus ou fausses déclarations = **fraude**, sévèrement punie. Ne jamais frauder : pénalités, intérêts, voire prison.\n\n**Stratégies légales :** Choisir les bons placements (PEA pour les actions, assurance-vie pour la diversification, Livret A pour la précaution). Profiter des réductions et crédits d'impôt (dons 66%, services à la personne 50%, Pinel...). Optimiser le choix PFU vs barème progressif selon ta tranche.",
                "highlight": False
              },
              {
                "title": "Page 2",
                "content": "**Pièges à éviter :** Les \"conseils\" qui promettent des économies miraculeuses (souvent fraude déguisée). Les dispositifs trop complexes que tu ne comprends pas. Et surtout : **oublier de déclarer**. Même si tu optimises, tu dois tout déclarer. Transparence totale = sécurité.\n\n**La règle d'or :** Optimise légalement, déclare tout. Consulte un professionnel reconnu (expert-comptable, conseiller fiscal) en cas de doute.",
                "highlight": False
              }
            ],
            "quizBlocks": [
              {
                "Question": "Quelle est la différence entre optimisation fiscale et fraude fiscale ?",
                "questionType": "multiple-choice",
                "options": ["Il n'y a pas de différence", "L'optimisation utilise les dispositifs légaux, la fraude cache des revenus", "L'optimisation est toujours illégale", "La fraude est légale"],
                "correctAnswer": "L'optimisation utilise les dispositifs légaux, la fraude cache des revenus",
                "explanationcorrect": "Exactement ! Optimisation = PEA, réductions d'impôt, dispositifs légaux. Fraude = cacher des revenus, fausses déclarations. L'une est encouragée, l'autre sévèrement punie.",
                "explanationfalse": "Non ! L'optimisation = utiliser les dispositifs légaux (PEA, crédits d'impôt...). La fraude = cacher des revenus. Optimiser = jouer le jeu. Frauder = tricher. Ne jamais frauder.",
                "points": 5
              },
              {
                "Question": "Tu dois déclarer tous tes revenus même si tu optimises ta fiscalité.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Absolument ! L'optimisation c'est utiliser les dispositifs légaux, pas cacher des revenus. Transparence totale. Si tu caches quelque chose = fraude.",
                "explanationfalse": "C'est vrai ! Même en optimisant (PEA, réductions...), tu dois TOUT déclarer. Cacher des revenus = fraude, pas optimisation. Transparence = sécurité.",
                "points": 5
              },
              {
                "Question": "Associe : A. Utiliser un PEA ; B. Cacher des revenus ; C. Profiter des réductions d'impôt (dons).",
                "questionType": "matching",
                "options": ["A. Utiliser un PEA", "1. Optimisation légale", "B. Cacher des revenus", "2. Fraude fiscale", "C. Réductions d'impôt (dons)", "1. Optimisation légale"],
                "correctAnswer": "A → 1, B → 2, C → 1",
                "explanationcorrect": "Parfait ! PEA et réductions d'impôt = optimisation légale. Cacher des revenus = fraude. Reste toujours dans la légalité.",
                "explanationfalse": "Revois : PEA et réductions d'impôt = optimisation légale. Cacher des revenus = fraude fiscale, sévèrement punie.",
                "points": 5
              },
              {
                "Question": "Pour optimiser ta fiscalité tu peux :",
                "questionType": "multiple-choice",
                "options": ["Cacher des revenus", "Utiliser les dispositifs légaux (PEA, réductions d'impôt...)", "Faire de fausses déclarations", "Ne rien déclarer"],
                "correctAnswer": "Utiliser les dispositifs légaux (PEA, réductions d'impôt...)",
                "explanationcorrect": "Exactement ! Utilise PEA, assurance-vie, réductions d'impôt (dons, services à la personne...). Ne jamais cacher des revenus ou faire de fausses déclarations.",
                "explanationfalse": "Non ! Pour optimiser légalement : PEA, assurance-vie, réductions d'impôt. Ne JAMAIS cacher des revenus ou faire de fausses déclarations = fraude.",
                "points": 5
              },
              {
                "Question": "Si tu es en tranche d'imposition élevée (30%+), le PFU de 30% est souvent plus avantageux que le barème pour les revenus de capitaux.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Parfait ! En tranche élevée le PFU 30% évite de payer 41% ou 45%. En tranche faible (0-11%) le barème peut être mieux. Compare les deux.",
                "explanationfalse": "C'est vrai ! En tranche 30%+ le PFU 30% est souvent plus avantageux. En tranche faible le barème progressif peut l'être. C'est ton droit de choisir.",
                "points": 5
              },
              {
                "Question": "Tu dois te méfier des conseils qui promettent des économies d'impôts miraculeuses.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Absolument ! Si c'est trop beau pour être vrai, c'est souvent une arnaque ou de la fraude déguisée. Consulte un professionnel reconnu (expert-comptable, conseiller fiscal).",
                "explanationfalse": "C'est vrai ! Les promesses miraculeuses cachent souvent de la fraude ou des arnaques. L'optimisation légale = dispositifs connus (PEA, réductions...). Méfie-toi.",
                "points": 5
              }
            ]
          }
        },
        {
          "title": "Livret A, PEA, assurance-vie : comparatif",
          "description": "Comparer les trois piliers de l'épargne française et choisir selon ses objectifs.",
          "order": 3,
          "difficulty": "medium",
          "estimatedDuration": 11,
          "content": {
            "textBlocks": [
              {
                "title": "Page 1",
                "content": "**Livret A :** Exonération totale, disponible à tout moment, plafond 22 950€. Idéal pour l'épargne de précaution (3 à 6 mois de dépenses). Pas de risque de perte en capital.\n\n**PEA :** Pour investir en actions (et ETF). Avantage fiscal après 5 ans (exonération impôts sur les plus-values, 17,2% prélèvements sociaux restent). Plafond 150 000€ de versements. À utiliser pour un objectif long terme (retraite, projet 5 ans+).",
                "highlight": False
              },
              {
                "title": "Page 2",
                "content": "**Assurance-vie :** Contrat multi-supports (fonds euros, unités de compte). Avantages fiscaux progressifs (après 8 ans : abattement 4 600€/9 200€, puis PFU 7,5%). Pas de plafond de versement. Idéal pour diversifier et préparer la retraite ou transmettre.\n\n**En résumé :** Précaution = Livret A. Investissement actions long terme = PEA. Diversification et transmission = Assurance-vie. Tu peux cumuler les trois selon tes objectifs.",
                "highlight": False
              }
            ],
            "quizBlocks": [
              {
                "Question": "Le Livret A a un plafond de versement.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Exactement ! Plafond 22 950€ (hors intérêts capitalisés). Au-delà, l'argent peut être sur un compte à terme ou un autre placement. LDDS : 12 000€.",
                "explanationfalse": "C'est vrai ! Livret A = 22 950€ max. LDDS = 12 000€. Au-delà il faut d'autres placements (PEA, assurance-vie, compte-titres...).",
                "points": 5
              },
              {
                "Question": "Le PEA est surtout adapté pour :",
                "questionType": "multiple-choice",
                "options": ["Épargne de précaution court terme", "Investir en actions sur le long terme (5 ans+)", "Placer sans risque", "Défiscaliser les loyers"],
                "correctAnswer": "Investir en actions sur le long terme (5 ans+)",
                "explanationcorrect": "Parfait ! Le PEA est fait pour investir en actions (ou ETF) avec un horizon 5 ans minimum pour profiter de l'exonération d'impôts sur les plus-values.",
                "explanationfalse": "Non ! Le PEA sert à investir en actions (ou ETF) sur le long terme. Avant 5 ans pas d'avantage fiscal. Pour la précaution = Livret A.",
                "points": 5
              },
              {
                "Question": "L'assurance-vie n'a pas de plafond de versement.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Exactement ! Contrairement au Livret A ou au PEA, tu peux verser autant que tu veux sur une assurance-vie. Les avantages fiscaux s'améliorent avec la durée (8 ans+).",
                "explanationfalse": "C'est vrai ! Pas de plafond sur l'assurance-vie. En revanche Livret A = 22 950€, PEA = 150 000€ de versements. L'assurance-vie permet de diversifier sans limite de montant.",
                "points": 5
              },
              {
                "Question": "Associe : A. Livret A ; B. PEA ; C. Assurance-vie.",
                "questionType": "matching",
                "options": ["A. Livret A", "1. Précaution, exonération totale", "B. PEA", "2. Actions, avantage après 5 ans", "C. Assurance-vie", "3. Diversification, avantage après 8 ans"],
                "correctAnswer": "A → 1, B → 2, C → 3",
                "explanationcorrect": "Parfait ! Livret A = précaution. PEA = actions long terme. Assurance-vie = diversification et transmission. Les trois sont complémentaires.",
                "explanationfalse": "Revois : Livret A = précaution défiscalisée ; PEA = actions avantage après 5 ans ; assurance-vie = diversification avantage après 8 ans.",
                "points": 5
              },
              {
                "Question": "Je peux cumuler Livret A, PEA et assurance-vie.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Absolument ! Beaucoup de Français ont les trois : Livret A pour la précaution, PEA pour les actions, assurance-vie pour diversifier. Chacun a son rôle.",
                "explanationfalse": "C'est vrai ! Tu peux (et c'est souvent recommandé) avoir les trois : précaution (Livret A), actions (PEA), diversification (assurance-vie).",
                "points": 5
              },
              {
                "Question": "Quel placement pour un objectif à 10 ans (retraite) ?",
                "questionType": "multiple-choice",
                "options": ["Uniquement Livret A", "PEA ou assurance-vie (long terme)", "Compte courant", "Argent liquide"],
                "correctAnswer": "PEA ou assurance-vie (long terme)",
                "explanationcorrect": "Exactement ! Pour 10 ans, PEA (actions) ou assurance-vie (fonds euros + UC) permettent de profiter des avantages fiscaux (5 ans pour PEA, 8 ans pour assurance-vie).",
                "explanationfalse": "Pour un objectif 10 ans, le Livret A est trop limité (plafond, rendement). PEA ou assurance-vie sont adaptés au long terme avec avantages fiscaux.",
                "points": 5
              }
            ]
          }
        },
        {
          "title": "PFU vs barème progressif : que choisir ?",
          "description": "Comprendre quand opter pour le PFU à 30% ou pour le barème progressif pour ses revenus de capitaux.",
          "order": 4,
          "difficulty": "medium",
          "estimatedDuration": 10,
          "content": {
            "textBlocks": [
              {
                "title": "Page 1",
                "content": "**Le PFU (Prélèvement Forfaitaire Unique)** = 30% en un seul prélèvement (12,8% impôt + 17,2% prélèvements sociaux). Il s'applique par défaut sur les intérêts, dividendes, plus-values des comptes-titres (et PEA/assurance-vie avant les délais d'avantage).\n\n**Le barème progressif** = tu intègres ces revenus dans ton revenu imposable et tu es taxé selon ta tranche (0%, 11%, 30%, 41%, 45%). Tu peux **choisir** entre les deux pour la plupart des revenus de capitaux (intérêts, dividendes, plus-values CTO).",
                "highlight": False
              },
              {
                "title": "Page 2",
                "content": "**Quand le PFU est avantageux :** Si tu es dans une tranche élevée (30%, 41%, 45%), payer 30% fixe évite de payer plus. **Quand le barème est avantageux :** Si tu es dans une tranche faible (0% ou 11%), intégrer dans tes revenus peut faire payer moins que 30%.\n\n**En pratique :** Fais une simulation (ou demande à ton conseiller / un outil en ligne). Une fois choisi, l'option s'applique à tous tes revenus de capitaux de l'année. La règle d'or : compare selon ta situation.",
                "highlight": False
              }
            ],
            "quizBlocks": [
              {
                "Question": "Le PFU de 30% comprend l'impôt et les prélèvements sociaux.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Exactement ! 30% = 12,8% d'impôt + 17,2% de prélèvements sociaux. C'est un prélèvement unique, forfaitaire.",
                "explanationfalse": "C'est vrai ! Le PFU de 30% = 12,8% impôt + 17,2% prélèvements sociaux. Un seul prélèvement, pas deux.",
                "points": 5
              },
              {
                "Question": "Tu peux choisir entre PFU et barème progressif pour les intérêts d'un compte d'épargne.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Parfait ! Pour la plupart des revenus de capitaux (intérêts, dividendes, plus-values CTO) tu as le choix. Compare selon ta tranche pour optimiser.",
                "explanationfalse": "C'est vrai ! Tu as le droit de choisir entre PFU 30% et barème progressif pour ces revenus. Une fois choisi, ça s'applique à tous tes revenus de capitaux de l'année.",
                "points": 5
              },
              {
                "Question": "Si tu es en tranche 45%, le PFU 30% est en général :",
                "questionType": "multiple-choice",
                "options": ["Moins avantageux que le barème", "Plus avantageux que le barème", "Identique", "Interdit"],
                "correctAnswer": "Plus avantageux que le barème",
                "explanationcorrect": "Exactement ! En tranche 45%, sans PFU tu paierais 45% (+ 17,2%). Le PFU à 30% total te fait payer moins. En tranche 0-11% c'est souvent l'inverse.",
                "explanationfalse": "En tranche élevée (41%, 45%) le PFU 30% est souvent plus avantageux car tu évites de payer 41% ou 45% sur ces revenus. En tranche faible le barème peut être mieux.",
                "points": 5
              },
              {
                "Question": "Le choix PFU ou barème s'applique à tous les revenus de capitaux de l'année.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Vrai",
                "explanationcorrect": "Oui ! Tu ne peux pas prendre le PFU pour une partie et le barème pour une autre. C'est un choix global pour l'année pour tes revenus de capitaux.",
                "explanationfalse": "C'est vrai ! Une fois que tu optes pour le PFU ou le barème, ça s'applique à l'ensemble de tes revenus de capitaux (intérêts, dividendes, plus-values concernées) pour l'année.",
                "points": 5
              },
              {
                "Question": "Associe : A. PFU 30% ; B. Barème progressif ; C. Tranche 0% ou 11%.",
                "questionType": "matching",
                "options": ["A. PFU 30%", "1. Souvent avantageux si tranche élevée", "B. Barème progressif", "2. Intégration dans le revenu imposable", "C. Tranche 0% ou 11%", "3. Barème souvent plus intéressant"],
                "correctAnswer": "A → 1, B → 2, C → 3",
                "explanationcorrect": "Parfait ! PFU = souvent mieux si tranche 30%+. Barème = intégration dans les revenus. En tranche faible le barème peut être plus avantageux que 30%.",
                "explanationfalse": "Revois : PFU 30% souvent avantageux en tranche élevée ; barème = intégration revenus ; en tranche faible (0-11%) le barème peut être mieux que le PFU.",
                "points": 5
              },
              {
                "Question": "Les prélèvements sociaux (17,2%) s'appliquent en plus du PFU ou du barème.",
                "questionType": "true-false",
                "options": ["Vrai", "Faux"],
                "correctAnswer": "Faux",
                "explanationcorrect": "Avec le PFU, les 30% incluent déjà les 17,2% (12,8% impôt + 17,2% prélèvements). Avec le barème, l'impôt est selon ta tranche et les prélèvements sociaux s'ajoutent selon les règles.",
                "explanationfalse": "Avec le PFU, les 30% = tout compris (12,8% + 17,2%). Avec le barème progressif, tu paies l'impôt selon ta tranche et les prélèvements sociaux selon les règles applicables.",
                "points": 5
              }
            ]
          }
        }
      ]
    }
  ]
}

def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(CHAPTERS, f, ensure_ascii=False, indent=2)
    print(f"Written: {OUTPUT_PATH}")
    print(f"Chapters: {len(CHAPTERS['chapters'])}")
    for ch in CHAPTERS["chapters"]:
        print(f"  - {ch['title']}: {len(ch['lessons'])} lessons")

if __name__ == "__main__":
    main()
