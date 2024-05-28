# AREC / the-cube

Die <strong>A</strong>ustrian <strong>R</strong>eal <strong>E</strong>state <strong>C</strong>hallenge unter <span class="text-muted">Ao.Univ.Prof. Dipl.-Ing. Mag.rer.soc.oec. Dr.techn.</span> <a href="https://www.tuwien.at/mwbw/im/ie/ifm/team-jobs/redlein-alexander">Alexander Redlein</a> ermöglicht es jedes Jahr vier ausgewählten StudentInnen beim <a href="https://me.stanford.edu/project-opportunity-me310abc">Kurs ME310</a> der Universität Stanford teilzunehmen.
In dem Kurs lernte ich als einer dieser Studenten, wie der Design Thinking Prozess funktioniert und dieser angewendet wird, um innovative Lösungen zu entwickeln, wie in unserem Fall um den CO<sub>2</sub> Fußabdruck von Bestandsgebäuden zu senken.
Der Kurs endet mit der <a href="https://violin-round-zh3n.squarespace.com/">EXPE</a>, einer öffentlichen Konferenz in der alle Forschungsergebnisse dargestellt werden müssen.

Hierzu wurde von uns eine Software entwickelt, um ein Gebäude zu simulieren und diesem verschiedene Komponenten zur CO<sub>2</sub> Reduktion nachzurüsten, um deren Auswirkung zu erforschen.
Ein intelligenter Algorithmus kümmert sich um die Gebäudesteuerung, um das Gebäude weiter zu optimieren, um noch einen größeren Effekt zu erwirken.

## backend

Das backend simuliert das gesamte Gebäude.
Es ist in *python* geschrieben und startet einen Stateful Server, der mit jedem Zugriff auf `/step` einen Schritt weiter die Simulation laufen lässt.

## frontend

Das frontend, welches in *VUE.js* geschrieben ist, stellt die Daten, die das backend berechnet User freundlich dar.
Es dient bei der EXPE zur Veranschaulichung unserer Forschungsergebnisse.

## Arduino
Im Zuge des Projektes wurde auch ein physisches Modell entwickelt.
Dieses wird mit einem Arduino gesteuert, welcher mit mehreren LED Streifen den Energiefluss in einem Gebäude darstellt.

# Sponsoren
Wir danken herzlichst unseren Sponsoren:

<img alt="BIG Logo" src="https://www.big.at/fileadmin/user_upload/05_Presse-News/5_3_Downloads/BIG_Logo_Langform_72dpi.jpg">
<img alt="BHÖ Logo" src="https://www.burghauptmannschaft.at/dam/jcr:70582199-a1d2-40ae-83d1-bf87717ab41b/BH%C3%96%20LOGO%20NEU.JPG">
<img alt="Simacek Logo" src="https://www.simacek.com/apps/ckfinder/userfiles/files/simacek_logo.png">
