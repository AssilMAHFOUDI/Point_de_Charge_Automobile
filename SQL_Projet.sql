#------------------------------------------------------------
#        Script MySQL.
#------------------------------------------------------------
use projectbase;

#------------------------------------------------------------
# Table: Amenageur
#------------------------------------------------------------

CREATE TABLE Amenageur(
        nom_amenageur     Varchar (150) NOT NULL ,
        contact_amenageur Varchar (150) NOT NULL
	,CONSTRAINT Amenageur_PK PRIMARY KEY (nom_amenageur)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Operateur
#------------------------------------------------------------

CREATE TABLE Operateur(
        nom_operateur       Varchar (150) NOT NULL ,
        contact_operateur   Varchar (150) NOT NULL ,
        telephone_operateur Varchar (150)
	,CONSTRAINT Operateur_PK PRIMARY KEY (nom_operateur,contact_operateur)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Station
#------------------------------------------------------------

CREATE TABLE Station(
        id_station_itinerance Varchar (150) NOT NULL ,
        nom_enseigne          Varchar (150) ,
        Nom_station           Varchar (150) ,
        implantation_station  Varchar (150) NOT NULL ,
        adresse_station       Varchar (150) ,
        code_insee_commune    Varchar (150) ,
        coordonneesXY         Varchar (150) ,
        nbre_pdc              Integer NOT NULL ,
        accessibilite_pmr     Varchar (150) ,
        restriction_gabarit   Varchar (150) ,
        station_deux_roues    Bool ,
        date_mise_en_service  Date ,
        date_maj              Date ,
        nom_amenageur         Varchar (150) NOT NULL ,
        nom_operateur         Varchar (150) NOT NULL ,
        contact_operateur     Varchar (150) NOT NULL
	,CONSTRAINT Station_PK PRIMARY KEY (id_station_itinerance)

	,CONSTRAINT Station_Amenageur_FK FOREIGN KEY (nom_amenageur) REFERENCES Amenageur(nom_amenageur)
	,CONSTRAINT Station_Operateur0_FK FOREIGN KEY (nom_operateur,contact_operateur) REFERENCES Operateur(nom_operateur,contact_operateur)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: PDC
#------------------------------------------------------------

CREATE TABLE PDC(
        id_pdc_itinerance     Varchar (150) NOT NULL ,
        puissance_nominale    Float NOT NULL ,
        prise_type_ef         Bool NOT NULL ,
        prise_type_2          Bool NOT NULL ,
        prise_type_combo_ccs  Bool NOT NULL ,
        prise_type_chademo    Bool NOT NULL ,
        prise_type_autre      Bool NOT NULL ,
        id_station_itinerance Varchar (150) NOT NULL
	,CONSTRAINT PDC_PK PRIMARY KEY (id_pdc_itinerance)

	,CONSTRAINT PDC_Station_FK FOREIGN KEY (id_station_itinerance) REFERENCES Station(id_station_itinerance)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Tarification
#------------------------------------------------------------

CREATE TABLE Tarification(
        id_pdc_itinerance Varchar (150) NOT NULL ,
        gratuit           Bool NOT NULL ,
        paiement_acte     Bool NOT NULL ,
        paiement_cb       Bool NOT NULL ,
        paiement_autre    Bool NOT NULL ,
        tarification      Varchar (150) 
	,CONSTRAINT Tarification_PK PRIMARY KEY (id_pdc_itinerance)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Acces
#------------------------------------------------------------

CREATE TABLE Acces(
        id_station_itinerance Varchar (150) NOT NULL ,
        condition_acces       Varchar (150) NOT NULL ,
        reservation           Bool NOT NULL ,
        horaires              Varchar (150) NOT NULL
	,CONSTRAINT Acces_PK PRIMARY KEY (id_station_itinerance)
)ENGINE=InnoDB;

