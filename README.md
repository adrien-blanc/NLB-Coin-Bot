# READ_ME - BOT Coin NLB
## Description
Ce projet a été crée dans l'objectif de fournir un petit BOT [Discord](https://discord.com/) sur mon serveur privé pour pouvoir jouer avec mes amis.
Ce BOT est le premier de ma longue série de BOT Discord, il n'est donc pas très évolué ... La "BDD" est stockée sous la forme d'un fichier JSON ce qui peut poser problème en lors d'insertion simultané en asynchrone de données dans cette dernière. 

## How to deploy
Remplacer tout en bas du fichier main.py, le token par le token de votre BOT. Vous trouverez votre token sur la page des [développeur](https://discord.com/developers) de Discord.

## Voici les commandes que vous pourrez utiliser avec le BOT NLB :

### COMMANDES PRINCIPALES :

**!balance <pseudo>** : Permet de voir l'état de vos comptes ou du compte d'un ami. | Permet également d'initialiser votre compte. | Ex : !balance ou !balance @Ursule

**!beg** : Permet de recevoir une somme aléatoire entre 0 et 10 (Limite : 3/jours)

**!rand <int>** : Permet de mettre en jeu une certaine somme de Coins (50% de chance de doubler cette somme | 50% de chance de la perdre). | Ex : !rand 50

**!rank** : Permet d'afficher le top 5 du serveur Nique La Bac.

**!giveaway** : Permet de lancer un giveaway. Attention vous payer de votre poche. (De préférence pour le choix du chanel choisissez le chanel #général que tout le monde le voit.)

**!bet** : Permet de lancer un pari. Vos coins doivent être dans votre  banque. (De préférence pour le choix du chanel choisissez le chanel #général que tout le monde le voit.)




### COMMANDES TRANSFERT Banque / Wallet :

Transférer des Coins dans votre banque : 

**!tC <int> **: Permet de transférer une somme définit dans votre banque. | Ex : !tC 50

**!tCAll** : Permet de transférer tout votre Wallet dans votre banque. 


#### Transférer des Coins dans votre Wallet :

**!gC <int>** : Permet de transférer une somme définit dans votre Wallet | Ex : !gC 50

**!gCAll** : Permet de transférer toute votre banque dans votre Wallet. 



#### Transférer des Coins User / User  :

Si vous voulez donner des Coins à votre meilleur ami (C'est franchement sympa) /!\ Vous ne pourrez donner qu'une fois par jour /!\  :

**!give <int> <pseudo> **: Permet de transférer une somme donnée à une personne choisit | Ex : !give 50 @Ursule


Si vous voulez voler quelques Coins à votre "meilleur" ami, juste Let's GO prenez-lui tout ! : 
/!\ ATTENTION /!\ Vous aurez 35% de chance de lui subtiliser la somme, en cas d'échec la somme sera débitée de votre compte et donnée à la victime pour compenser ce traumatisme que vous lui avez fait vivre. 

**!ludoVoleur <int> <pseudo>** : Permet d'avoir une chance de voler les précieux Coins d'une personne. | Ex : !ludoVoleur 50 @Ursule


### COMMANDES AVANTAGES Coins  :

C'est bien beau d'acquérir tous ces Coins, mais a quoi servent-ils ? 
Voici une liste des commandes à utiliser contre des Coins : 

Kick un "ami" du serveur pendant 1 journée : 

Prix : 5000 Coins
**!kick <pseudo> ** : Permet de kick une personne du serveur pendant 1 jour  (Des exceptions pourront-être faites si le jour en question est important ! Exemple : Kick Ludo lorsque l'on a un exam de prog en distanciel ne sera pas toléré !!! ) | Ex : !kick @Ursule


Mute (vocal) une personne de votre choix :

Prix : **2000 Coins**
**!mute <pseudo>** : Permet de mute une personne du serveur pendant 1 jour (Des exceptions pourront-être faites si le jour en question est important !) | Ex : !mute @Ursule

### COMMANDES OH SHIT :

Si vous venez a être à court de Coins, ne pas paniquer, une commande est faites pour vous : 

**!pitierMonsieur** : Vous redonne 50 Coins gratuitement si votre Wallet et votre banque sont inférieurs à 10 Coins.

### REGLES PRINCIPALES :

Les Coins mis dans votre banque sont en sécurité, personne ne pourra vous les voler, même avec un !ludoVoleur sauvage.

Toutes les heures, toutes les personnes possédant un compte recevrons 5 Coins complétement gratuitement (120/jour).

Tous les jours à 22 Heures, un GiveAway de 500 Coins se lancera automatiquement dans le salon #général. (Il durera 30 minutes)

Tous les jours à 23 Heures, vos Coins mis en banque vous feront gagner des intérêts (1%)

Tous les jours à minuit les Beg, les Give et les Pitier Monsieur seront de nouveau disponible pour tous.
