# DeepDoggo: Detecting Viral Reads in Dog Cancer RNA Data Using Deep Learning

## Introduction
DeepDoggo est une méthode basée sur l'apprentissage profond pour détecter des séquences virales dans les données d'ARN issues de cancers canins. Ce projet est inspiré de l'approche décrite par Elbasir et al., appliquée aux séquences de chiens en raison de restrictions d'accès aux bases de données humaines. 

L'objectif est de déterminer si des séquences virales peuvent être identifiées dans des cancers canins similaires à ceux humains, ainsi que dans des cancers spécifiques aux chiens comme le **tumor vénérien transmissible canin (CTVT)**.

## Fonctionnalités
- Prétraitement des données génomiques pour les adapter à un modèle d'apprentissage profond.
- Implémentation d'un modèle convolutionnel pour classifier les séquences virales et non-virales.
- Reconstruction et analyse des séquences prédictives pour évaluer leur similarité avec des références connues.

## Prérequis
- **Python 3.8+**
- **TensorFlow 2.x**
- **Keras**
- **NumPy**
- Outils pour le traitement des données génomiques comme **FastQC**, **Bowtie2**, **seqtk**, **bedtools** et **samtools**

## Données
Les données utilisées pour ce projet comprennent :
1. **Données de cancers canins** : Collectées depuis des bases comme l'**European Nucleotide Archive** et **PubMed**.
2. **Base de données virales** : Obtenue via "Virus-Host DB" pour compiler 74 virus associés aux chiens.
3. **Formatage des séquences** : Les séquences ont été découpées en fragments de 50 pb (paires de bases) avec chevauchement pour équilibrer les données entre lectures virales et non-virales.

## Installation et utilisation
1. Clonez ce dépôt Git :
   ```bash
   git clone https://github.com/NoahLacchini/Bioinformatic.git
   cd Bioinformatic
   ```
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation
### Prétraitement des données
1. Téléchargez et préparez les fichiers FASTQ pour chaque type de cancer.
2. Convertissez et alignez les séquences avec Bowtie2 :
   ```bash
   bowtie2 -x reference -1 input_1.fastq -2 input_2.fastq -S output.sam
   ```
3. Filtrez les lectures non mappées et convertissez-les en fichiers FASTA à l'aide de *fastq_to_fasta.sh*.
4. Split the data using *Splitdata.py*
5. Use the different functions of *DeepLearningFinals.py*


## Résultats
### Analyse des résultats obtenus
Après l'entraînement du modèle, nous avons effectué des prédictions sur les données de test et les séquences extraites des échantillons de cancer canin. Les résultats détaillés sont les suivants :

#### Phases d'entraînement et de prédiction
- **Durée d'entraînement** : Le modèle a été entraîné pendant environ 20 heures, atteignant 25 époques sur les 150 prévues, en raison de limitations matérielles. Cela a réduit la capacité du modèle à converger vers un état optimal.
- **Durée de la prédiction** : La phase de prédiction a duré 5 heures, au cours desquelles le modèle a classifié les séquences comme virales ou non virales avec un seuil de 0,5 pour la classification.

#### Reconstruction des séquences prédictives
- **Assemblage des séquences** : Les séquences classifiées comme virales ont été assemblées à l'aide de SPAdes, produisant 20 contigs de longueur variable (de 35 à 959 paires de bases).
- **Analyse avec BLAST** : Chaque contig a été comparé à une base de données de séquences nucléotidiques. Les résultats montrent que toutes les séquences reconstruites correspondent exclusivement à des séquences mitochondriales canines. Voici un résumé :
  - Séquences mitochondriales provenant principalement de **Canis lupus familiaris** (chien domestique).
  - Présence de séquences associées à des sous-espèces comme **Canis lupus dingo**.

#### Observations spécifiques
- Les séquences identifiées incluent des régions spécifiques au Labrador Retriever, indiquant que certains échantillons de cancer proviennent probablement de cette race.
- Aucune séquence virale n'a été détectée, suggérant soit l'absence de séquences virales dans les données initiales, soit une performance limitée du modèle.

#### Limitations des résultats
1. **Qualité des données** : Les données utilisées ne contenaient peut-être pas de séquences virales détectables.
2. **Paramétrage du modèle** : Les hyperparamètres n'ont pas été optimisés en raison de contraintes de temps et de matériel.
3. **Profondeur d'entraînement insuffisante** : Avec seulement 25 époques, le modèle n'a pas pleinement appris les caractéristiques des séquences virales.

### Conclusion
Bien que les résultats n'aient pas révélé de séquences virales, le projet a permis de suivre une approche méthodique et reproductible pour analyser les séquences génomiques. Des ajustements futurs pourraient inclure un entraînement plus long, une optimisation des hyperparamètres et l'utilisation de données plus riches en séquences virales potentielles.

## Contributions
- **Noah Lacchini**  
- **Ayoub Adib**

## Références
- Elbasir et al., "A deep learning approach reveals unexplored landscape of viral expression in cancer" (2023)
- [Projet VirnaTrap](https://github.com/AuslanderLab/virnatrap)
