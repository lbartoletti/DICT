# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DICT_dialog_wizard
                                 A QGIS plugin
 DICT
                             -------------------
        begin                : 2015-08-19
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Loïc BARTOLETTI
        email                : lbartoletti@tuxfamily.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtXml import *
from PyQt4 import uic
from qgis.core import *
from qgis.gui import *
from qgis.utils import iface

import tempfile
import shutil
import os
import datetime
import codecs

try:
    import popplerqt4
    POPPLER = True
except:
    POPPLER = False

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'DICT_dialog_wizard.ui'))


class DICTDialogWizard(QDialog, FORM_CLASS):

    def __init__(self, champs, parent=None):
        """Constructor."""
        super(DICTDialogWizard, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.ref_DICT = champs['ReferenceExploitant']
        self.champs = champs

        self.RepImpossible.clicked.connect(self.chkRepImpossible)
        self.PasConcerne.clicked.connect(self.chkPasConcerne)
        self.Concerne.clicked.connect(self.chkConcerne)
        self.ModifEnCours.clicked.connect(self.chkModifEnCours)
        self.PlansJoints.clicked.connect(self.chkPlansJoints)
        self.ReunionChantierCase.clicked.connect(self.chkReunionChantierCase)
        self.DateRDV.clicked.connect(self.chkDateRDV)
        self.RDVparDeclarant.clicked.connect(self.chkRDVparDeclarant)
        self.Ref1.textEdited.connect(self.editRef1)

        self.initWizard()

    def chkRepImpossible(self):
        if self.RepImpossible.isChecked():
            self.InfoPreciser.setEnabled(True)
        else:
            self.InfoPreciser.setEnabled(False)

    def chkPasConcerne(self):
        if self.PasConcerne.isChecked():
            self.DistanceReseau.setEnabled(True)
        else:
            self.DistanceReseau.setEnabled(False)

    def chkConcerne(self):
        if self.Concerne.isChecked():
            self.CategorieReseau1.setEnabled(True)
            self.CategorieReseau2.setEnabled(True)
            self.CategorieReseau3.setEnabled(True)
        else:
            self.CategorieReseau1.setEnabled(False)
            self.CategorieReseau2.setEnabled(False)
            self.CategorieReseau3.setEnabled(False)

    def chkModifEnCours(self):
        if self.ModifEnCours.isChecked():
            self.RepresentantExploitant.setEnabled(True)
            self.TelModification.setEnabled(True)
        else:
            self.RepresentantExploitant.setEnabled(False)
            self.TelModification.setEnabled(False)

    def chkPlansJoints(self):
        if self.PlansJoints.isChecked():
            self.Ref1.setEnabled(True)
            self.Echelle1.setEnabled(True)
            self.EditionPlan1.setEnabled(True)
            self.Sensible1.setEnabled(True)
            self.Profondeur1.setEnabled(True)
            self.Materiau1.setEnabled(True)
            if len(self.Ref1.text()) > 0:
                self.Ref2.setEnabled(True)
                self.Echelle2.setEnabled(True)
                self.EditionPlan2.setEnabled(True)
                self.Sensible2.setEnabled(True)
                self.Profondeur2.setEnabled(True)
                self.Materiau2.setEnabled(True)

        else:
            self.Ref1.setEnabled(False)
            self.Echelle1.setEnabled(False)
            self.EditionPlan1.setEnabled(False)
            self.Sensible1.setEnabled(False)
            self.Profondeur1.setEnabled(False)
            self.Materiau1.setEnabled(False)
            self.Ref2.setEnabled(False)
            self.Echelle2.setEnabled(False)
            self.EditionPlan2.setEnabled(False)
            self.Sensible2.setEnabled(False)
            self.Profondeur2.setEnabled(False)
            self.Materiau2.setEnabled(False)

    def chkReunionChantierCase(self):
        if self.ReunionChantierCase.isChecked():
            self.DateRDV.setEnabled(True)
            self.RDVparDeclarant.setEnabled(True)
            if self.DateRDV.isChecked():
                self.Reunion.setEnabled(True)
            else:
                self.Reunion.setEnabled(False)
            if self.RDVparDeclarant.isChecked():
                self.AppelNonConcl.setEnabled(True)
            else:
                self.AppelNonConcl.setEnabled(False)
        else:
            self.DateRDV.setEnabled(False)
            self.RDVparDeclarant.setEnabled(False)
            self.AppelNonConcl.setEnabled(False)
            self.Reunion.setEnabled(False)

    def chkDateRDV(self):
        if self.DateRDV.isChecked():
            self.Reunion.setEnabled(True)
        else:
            self.Reunion.setEnabled(False)

    def chkRDVparDeclarant(self):
        if self.RDVparDeclarant.isChecked():
            self.AppelNonConcl.setEnabled(True)
        else:
            self.AppelNonConcl.setEnabled(False)

    def editRef1(self, nText):
        if len(nText) > 0:
            self.Ref2.setEnabled(True)
            self.Echelle2.setEnabled(True)
            self.EditionPlan2.setEnabled(True)
            self.Sensible2.setEnabled(True)
            self.Profondeur2.setEnabled(True)
            self.Materiau2.setEnabled(True)
        else:
            self.Ref2.setEnabled(False)
            self.Echelle2.setEnabled(False)
            self.EditionPlan2.setEnabled(False)
            self.Sensible2.setEnabled(False)
            self.Profondeur2.setEnabled(False)
            self.Materiau2.setEnabled(False)

    def initWizard(self):
        self.line = [
            [
             self.Denomination,
             self.champs['dest_Denomination'],
             u"dest_Denomination",
             3
             ],
            [
             self.ComplementAdresse,
             self.champs['dest_ComplementAdresse'],
             u"dest_ComplementAdresse",
             4
            ],
            [
             self.NoVoie,
             self.champs['dest_NoVoie'],
             u"dest_NoVoie",
             5
            ],
            [
             self.LieuditBP,
             self.champs['dest_LieuditBP'],
             u"dest_LieuditBP",
             6
            ],
            [
             self.CodePostal,
             self.champs['dest_CodePostal'],
             u"dest_CodePostal",
             7
            ],
            [
             self.Commune,
             self.champs['dest_Commune'],
             u"dest_Commune",
             8
            ],
            [
             self.Pays,
             self.champs['dest_Pays'],
             u"dest_Pays",
             9
            ],
            [
             self.NoGU,
             self.champs['NoGu'],
             u"NoGU",
             10
            ],
            [
             self.ReferenceExploitant,
             self.champs['ReferenceExploitant'],
             u"ReferenceExploitant",
             11
            ],
            [
             self.NoAffaireDeclarant,
             self.champs['NoAffaireDeclarant'],
             u"NoAffaireDeclarant",
             12
            ],
            [
             self.Personne_Contacter,
             self.champs['Personne_Contacter'],
             u"Personne_Contacter",
             13
            ],
            [
             self.CommuneTravaux,
             self.champs['communePrincipale'],
             u"CommuneTravaux",
             17
            ],
            [
             self.AdresseTravaux,
             self.champs['AdresseTravaux'],
             u"AdresseTravaux",
             18
            ],
            [
             self.RaisonSocialeExploitant,
             QSettings().value("/DICT/coordDenom"),
             u"RaisonSocialeExploitant",
             19
            ],
            [
             self.ContactExploitant,
             QSettings().value("/DICT/coordPersonne"),
             u"ContactExploitant",
             20
            ],
            [
             self.NoVoieExploitant,
             QSettings().value("/DICT/coordNumVoie"),
             u"NoVoieExploitant",
             21
            ],
            [
             self.LieuditBPExploitant,
             QSettings().value("/DICT/coordBP"),
             u"LieuditBPExploitant",
             22
            ],
            [
             self.CodePostalExploitant,
             QSettings().value("/DICT/coordCP"),
             u"CodePostalExploitant",
             23
            ],
            [
             self.CommuneExploitant,
             QSettings().value("/DICT/coordCommune"),
             u"CommuneExploitant",
             24
            ],
            [
             self.TelExploitant,
             QSettings().value("/DICT/coordTel"),
             u"TelExploitant",
             25
            ],
            [
             self.FaxExploitant,
             QSettings().value("/DICT/coordFax"),
             u"FaxExploitant",
             26
            ],
            [
             self.InfoPreciser,
             u'',
             u"InfoPreciser",
             28
            ],
            [
             self.DistanceReseau,
             u'',
             u"DistanceReseau",
             30
            ],
            [
             self.ModifPrevue,
             u'',
             u"ModifPrevue",
             35
            ],
            [
             self.RepresentantExploitant,
             u'',
             u"RepresentantExploitant",
             37
            ],
            [
             self.TelModification,
             u'',
             u"TelModification",
             38
            ],
            [
             self.Ref1,
             u'',
             u"Ref1",
             40
            ],
            [
             self.Ref2,
             u'',
             u"Ref2",
             48
            ],
            [
             self.Echelle1,
             u'',
             u"Echelle1",
             41
            ],
            [
             self.Echelle2,
             u'',
             u"Echelle2",
             49
            ],
            [
             self.Profondeur1,
             u'',
             u"Profondeur1",
             46
            ],
            [
             self.Profondeur2,
             u'',
             u"Profondeur2",
             54
            ],
            [
             self.Materiau1,
             u'',
             u"Materiau1",
             47
            ],
            [
             self.Materiau2,
             u'',
             u"Materiau2",
             55
            ],
            [
             self.Recommandations,
             u'',
             u"Recommandations",
             70
            ],
            [
             self.RubriquesGuide,
             u'',
             u"RubriquesGuide",
             71
            ],
            [
             self.MesuresSecurite2,
             u'',
             u"MesuresSecurite2",
             75
            ],
            [
             self.MesuresSecurite,
             u'',
             u"MesuresSecurite",
             74
            ],
            [
             self.TelEndommagement,
             QSettings().value("/DICT/TelEndommagement", u''),
             u"TelEndommagement",
             77
            ],
            [
             self.Endommagement,
             QSettings().value("/DICT/Endommagement", u''),
             u"Endommagement",
             78
            ],
            [
             self.NomResponsableDossier,
             QSettings().value("/DICT/respNom", u''),
             u"NomResponsableDossier",
             79
            ],
            [
             self.DesignationService,
             QSettings().value("/DICT/respService", u''),
             u"DesignationService",
             80
            ],
            [
             self.TelResponsableDossier,
             QSettings().value("/DICT/respTel", u''),
             u"TelResponsableDossier",
             81
            ],
            [
             self.NomSignataire,
             QSettings().value("/DICT/signNom", u''),
             u"NomSignataire",
             82
            ],
            [
             self.NbPJ,
             u'1',
             u"NbPJ",
             88
            ],
            [
             self.signSignataire,
             QSettings().value("/DICT/signSignature", u''),
             u"signSignataire"
             # n'est pas un champs dans le cerfa PDF
            ]
        ]

        for i in self.line:
            i[0].setText(i[1])

        for i in self.findChildren(QDateEdit):
            i.setDate(datetime.date.today())

        for i in self.findChildren(QDateTimeEdit):
            i.setDate(datetime.date.today())

        # Date réception
        self.dateReceptionDeclaration.setDate(self.champs['dateRecep'])

        # CheckBox DT/DICT/DC
        # pour possible/impossible
        self.champs['Possible'] = False
        self.champs['Impossible'] = False
        for i in self.findChildren(QRadioButton):
            if self.champs[i.objectName()]:
                i.setChecked(True)
            else:
                i.setChecked(False)

        if QSettings().value("/DICT/casDT") == "true" \
           and self.Recepisse_DT.isChecked():
            self.PasClasseACase.setChecked(True)

    def saveChangeQGis(self):
        def formulaireQGis(titre, path):
            myMapRenderer = iface.mapCanvas().mapSettings()
            # Load template from file
            myComposition = QgsComposition(myMapRenderer)
            myTemplateFile = file(path, 'rt')
            myTemplateContent = myTemplateFile.read()
            myTemplateFile.close()
            myDocument = QDomDocument()
            myDocument.setContent(myTemplateContent)
            myComposition.loadFromTemplate(myDocument)

            printer = QPrinter()
            printer.setOutputFormat(QPrinter.PdfFormat)

            # Sortie
            out_dir = QSettings().value("/DICT/configRep")
            if QDir(out_dir).exists() is False or out_dir is None:
                out_dir = str(QDir.homePath())

            out = os.path.join(out_dir,
                               QSettings().value("/DICT/prefRecep", u"") +
                               titre +
                               QSettings().value("/DICT/sufRecep", u"") +
                               ".pdf")

            printer.setOutputFileName(out)
            printer.setPaperSize(QSizeF(myComposition.paperWidth(),
                                        myComposition.paperHeight()),
                                 QPrinter.Millimeter)
            printer.setFullPage(True)
            printer.setColorMode(QPrinter.Color)
            printer.setResolution(myComposition.printResolution())

            pdfPainter = QPainter(printer)
            paperRectMM = printer.pageRect(QPrinter.Millimeter)
            paperRectPixel = printer.pageRect(QPrinter.DevicePixel)
            myComposition.render(pdfPainter, paperRectPixel, paperRectMM)
            pdfPainter.end()

            return out

        path = os.path.join(os.path.dirname(__file__), "formulaire_pdf")
        fdt, form = tempfile.mkstemp()
        formulaire = os.path.join(path, "Formulaire_DICT.qpt")
        shutil.copy2(formulaire, form)
        fdn, newfile = tempfile.mkstemp()

        f = codecs.open(form, encoding="utf-8")
        n = codecs.open(newfile, "w", encoding="utf-8")

        contenu = f.read()

        # Image du CERFA
        contenu = contenu.replace("CHEMIN_VERS_IMAGE", path)

        # Change contenu lignes
        for i in self.line:
            if i[0].isEnabled():
                contenu = contenu.replace(i[2], Qt.escape(i[0].text()))
            else:
                contenu = contenu.replace(i[2], u"")

        # Change contenu checkbox
        for i in self.findChildren(QCheckBox):
            name = i.objectName()
            if i.isChecked():
                contenu = contenu.replace(name, u"X")
            else:
                contenu = contenu.replace(name, u"")

        # Change contenu radio
        for i in self.findChildren(QRadioButton):
            name = i.objectName()
            if i.isChecked():
                contenu = contenu.replace(name, u"X")
            else:
                contenu = contenu.replace(name, u"")

        # Change dateTime
        for i in self.findChildren(QDateTimeEdit):
            name = i.objectName()
            date_obj = i.date()
            time_obj = i.time()
            ok = True  # cas particulier des EditionsPlans
            if name == 'EditionPlan1' and len(self.Ref1.text()) == 0:
                ok = False
            if name == 'EditionPlan2' and (len(self.Ref1.text()) == 0 or
                                           len(self.Ref2.text()) == 0):
                ok = False

            if i.isEnabled() and ok:
                contenu = contenu.replace("Jour" + name,
                                          str(date_obj.day()).rjust(2, '0'))
                contenu = contenu.replace("Mois" + name,
                                          str(date_obj.month()).rjust(2, '0'))
                contenu = contenu.replace("Annee" + name,
                                          str(date_obj.year()).rjust(4))
                contenu = contenu.replace("Heure" + name,
                                          str(time_obj.hour()).rjust(2, '0'))
                contenu = contenu.replace("Minute" + name,
                                          str(time_obj.minute()).rjust(2, '0'))
            else:
                contenu = contenu.replace("Jour"+name, u"")
                contenu = contenu.replace("Mois"+name, u"")
                contenu = contenu.replace("Annee"+name, u"")
                contenu = contenu.replace("Heure"+name, u"")
                contenu = contenu.replace("Minute"+name, u"")

        # Change Menu
        for i in self.findChildren(QComboBox):
            name = i.objectName()
            if i.isEnabled():
                contenu = contenu.replace(name, i.currentText())
            else:
                contenu = contenu.replace(name, u"")

        n.write(contenu)

        n.close()
        f.close()

        shutil.copy2(newfile, form)

        # A changer
        titre = self.ReferenceExploitant.text()
        pdf = formulaireQGis(titre, form)

        os.close(fdt)
        os.remove(form)
        os.close(fdn)
        os.remove(newfile)

        return titre, pdf

    def saveChangePoppler(self):
        def findId(l, txt):
            id_f = -1
            for i, j in enumerate(l):
                if txt == j.name():
                    id_f = i
                    break
            return id_f

        if POPPLER is False:
            return None, None

        path = os.path.join(os.path.dirname(__file__), "formulaire_pdf")
        formulaire = os.path.join(path, 'cerfa_14435-03.pdf')

        doc = popplerqt4.Poppler.Document.load(formulaire)

        try:
            page = doc.page(0)
        except:
            return None, None

        fields = page.formFields()

        # Change contenu lignes
        for i in self.line:
            if i[0].isEnabled():
                fields[i[1]].setText(i[0].text())

        # Change contenu checkbox
        for i in self.findChildren(QCheckBox):
            id_f = findId(fields, i.objectName())
            if id_f != -1:
                if i.isChecked():
                    fields[id_f].setState(True)

        # Change contenu radio
        for i in self.findChildren(QRadioButton):
            name = i.objectName()
            id_f = findId(fields, name)
            if id_f != -1:
                if i.isChecked():
                    fields[id_f].setState(True)
            else:
                # impossible d'automatiser puisqu'il n'y a pas
                # de nom dans les champs du pdf
                if name == "Possible":
                    if i.isChecked():
                        fields[72].setState(True)
                elif name == "Impossible":
                    if i.isChecked():
                        fields[73].setState(True)

        # Change dateTime
        for i in self.findChildren(QDateTimeEdit):
            name = i.objectName()
            date_obj = i.date()
            time_obj = i.time()
            ok = True  # cas particulier des EditionsPlans
            if name == 'EditionPlan1' and len(self.Ref1.text()) == 0:
                ok = False
            if name == 'EditionPlan2' and (len(self.Ref1.text()) == 0 or
                                           len(self.Ref2.text()) == 0):
                ok = False

            if i.isEnabled() and ok:
                # Cas particulier de AppelNonConcl_ Jour Mois et Annee
                ext = "AppelNonConcl"
                if name.find(ext) >= 0:
                    id_f = findId(fields, ext + "_" + "Jour")
                    if id_f != -1:
                        fields[id_f].setText(str(date_obj.day()).rjust(2, '0'))
                    id_f = findId(fields, ext + "_" + "Mois")
                    if id_f != -1:
                        fields[id_f].setText(str(date_obj.month()).rjust(2, '0'))
                    id_f = findId(fields, ext + "_" + "Annee")
                    if id_f != -1:
                        fields[id_f].setText(str(date_obj.year()).rjust(4))
                else:
                    id_f = findId(fields, "Jour" + name)
                    if id_f != -1:
                        fields[id_f].setText(str(date_obj.day()).rjust(2, '0'))
                    id_f = findId(fields, "Mois" + name)
                    if id_f != -1:
                        fields[id_f].setText(str(date_obj.month()).rjust(2, '0'))

                    id_f = findId(fields, "Annee" + name)
                    if id_f != -1:
                        fields[id_f].setText(str(date_obj.year()).rjust(4))

                    # cas particulier des années
                    # Les champs EditionsPlan ne sont pas
                    # identiques pour les années, ils se nomment :
                    # AnneeEditionN au lieu de AnneeEditionPlanN
                    # où N est le numéro...
                    len_p = len('Plan')
                    id_p = name.find('Plan')
                    name_alt = name[:id_p]+name[id_p+len_p:]
                    id_f = findId(fields, "Annee" + name_alt)
                    if id_f != -1:
                        fields[id_f].setText(str(date_obj.year()).rjust(4))

                    id_f = findId(fields, "Heure" + name)
                    if id_f != -1:
                        fields[id_f].setText(str(time_obj.hour()).rjust(2, '0'))
                    id_f = findId(fields, "Minute" + name)
                    if id_f != -1:
                        fields[id_f].setText(str(time_obj.minute()).rjust(2, '0'))

        # Change Menu
        for i in self.findChildren(QComboBox):
            name = i.objectName()
            id_f = findId(fields, name)
            if id_f != -1:
                if i.isEnabled():
                    fields[id_f].setCurrentChoices([i.currentIndex()])
                else:
                    fields[id_f].setCurrentChoices([0])

        # A changer
        titre = self.ReferenceExploitant.text()

        # Sortie
        out_dir = QSettings().value("/DICT/configRep")
        if QDir(out_dir).exists() is False or out_dir is None:
            out_dir = str(QDir.homePath())

        out = os.path.join(out_dir, QSettings().value("/DICT/prefRecep", u"") +
                           titre + QSettings().value("/DICT/sufRecep", u"") +
                           ".pdf")

        pdf = doc.pdfConverter()
        pdf.setOutputFileName(out)
        pdf.setPDFOptions(popplerqt4.Poppler.PDFConverter.WithChanges)
        pdf.convert()

        return titre, out
