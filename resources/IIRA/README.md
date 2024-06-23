<a name="readme-top"></a>
[![MIT License][license-shield]][license-url]
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/timokubera/IIRA">
    <img src="https://raw.githubusercontent.com/TimoKubera/IIRA/main/data/icons/intrarater_512px.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center"><b>IIRA</b></h3>

  <p align="center">
  <b>I</b>ntra- and <b>I</b>nterrater <b>R</b>eliability <b>A</b>nalyses
    <br />
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Inhalt</summary>
  <ol>
    <li>
      <a href="#about-the-project">Über das Projekt</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#requirements">Requirements</a>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">Lizenz</a></li>
    <li><a href="#contact">Kontakt</a></li>
  </ol>
</details>

<a name="about-the-project"></a>
<!-- ABOUT THE PROJECT -->
## Über das Projekt

IIRA kann verwendet werden, um Reliabilitätsuntersuchungen von Datensätzen vorzunehmen. Es kann sowohl die Interrater-Reliabilität analysiert werden, als auch die Intrarater-Reliabilität.
</br></br>
<details>
    <summary>Interrater-Reliabilität</summary>
    <p>Die Interrater-Reliabilität, oder Urteilerübereinstimmung, gibt das Ausmaß der Übereinstimmung der Einschätzungsergebnisse von unterschiedlichen Bewertern an.</p>
</details>
<details>
    <summary>Intrarater-Reliabilität</summary>
    <p>Die Intrarater-Reliabilität gibt das Ausmaß der Übereinstimmung der Einschätzungsergebnisse von einem Bewerter, zu unterschiedlichen Bewertungszeitpunkten, an.</p>
</details>
</br>
Darüber hinaus kann die Software verwendet werden, um Datensätze zu labeln.</br></br>

Anwendungen:
* Die Reliabilitätsuntersuchungen können eingesetzt werden, um Aussagen über die Reproduzierbarkeit von Datensätzen zu treffen.
  * z.B. bei Test- und Trainingsdatensätze, die in Supervised-Machine-Learning-Modellen eingesetzt werden.
  * oder, die in klinischen Studien eingesetzt werden
* Analoge Anwendungsfälle beim Labeln der Daten 

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<a name="built-with"></a>
### Built With

Eine kleine Übersicht der wichtigsten Sprachen und Frameworks.
Eine vollständige Liste der requirements findest du unter <a href="#requirements">Requirements</a>.

* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
* ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<a name="requirements"></a>
<!-- GETTING STARTED -->
## Requirements
Es ist Python>=3.6 erforderlich, um das Programm auszuführen, sowie die Installation der folgenden Packages:
* openpyxl
* odfpy
* xlrd
* numpy
* pandas
* irrCAC
* pingouin
* xlsxwriter
* pillow

### Installation

1. Die Repo von <a href="https://github.com/timokubera/iira">GitHub</a> clonen.
2. Abhängigkeiten installieren
   ```sh
   cd ~/path/to/IIRA
   pip3 install -r requirements.txt
   ```
3. Programm ausführen
   ```sh
   python app.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<a name="usage"></a>
<!-- USAGE EXAMPLES -->
## Usage
1. Analysieren Use Case

Bevor ein Datensatz analysiert werden kann, muss der SW-User vorab einige Informationen übermitteln.
Diese umfassen:
* Skalenformat der Daten auswählen (nominal, ordinal, intervall, rational)
* Datei importieren
  * Kategorienamen spezifizieren (bei diskretem Skalenformat)
* Auswahl der Bewerter, deren Bewertungen analysiert werden sollen
* Auswahl der Metriken, mit denen die Analyse durchgeführt werden soll
* Auswahl der Gewichte für die Metriken
* Analyse starten

Es stehen die folgenden Metriken für die Analysen zur Auswahl:
* Cohen's Kappa
* Conger's Kappa
* Fleiss' Kappa
* Krippendorff's Alpha
* Gwet's AC
* ICC

Nachdem die Informationen angegeben worden sind, kann eine Analyse durchgeführt und als Excel-Datei exportiert werden.

Die Ergebnisse von Intrarater-Analysen von mehreren Bewertern, werden auf dem folgenden Bild dargestellt.

<img src="https://raw.githubusercontent.com/TimoKubera/IIRA/main/data/img/analyse.png" alt="analyse-results">

Jedes Fenster in der GUI ist mit einem Hilfe-Button ausgestattet, in dem Informationen zum gerade geöffneten Fenster bereitgestellt werden.
Das Hilfefenster bzgl. der Ergebnisse liefert beispielsweise eine Interpretationsmöglichkeit der Ergebnisse nach Landis & Koch.

<img src="https://raw.githubusercontent.com/TimoKubera/IIRA/main/data/img/helpframe_interpretation.png" alt="help-interpretation" width="420" heigth="700">

2. Bewerten Use Case
Um einen Datensatz zu bewerten, ist das Vorgehen ähnlich:
* Skalenformat der Daten auswählen (nominal, ordinal, intervall, rational)
* Datei importieren
  * Kategorienamen spezifizieren (bei diskretem Skalenformat)
* Bewertungen starten

Bevor die Bewertungssession gestartet wird, hat der Bewerter die Möglichkeit, die Reihenfolge der Bewertungselemente zu randomisieren. Dadurch soll sichergestellt werden, dass sich der Bewerter nicht an Patterns gewöhnen kann, die den Bewertungsvorgang beeinflußen könnten.

Die Bewertung wird anschließend in dem folgenden Fenster vorgenommen.

<img src="https://raw.githubusercontent.com/TimoKubera/IIRA/main/data/img/rate.png" alt="help-interpretation">

Beim Speichern der Bewertungssession, werden sowohl die vorgenommenen Bewertungen gespeichert, als auch ein Bewertername, bzw. eine Bewerter-ID.
Die Bewerter-ID entspricht dem aktuell angemeldeten Profil und kann während der Bewertungssession über den entsprechenden Button, oben links, geändert werden.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a name="license"></a>
<!-- LICENSE -->
## Lizenz

Das Projekt wurde unter der MIT-Lizenz veröffentlicht. Siehe in die `LICENSE.txt` für weitere Informationen.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<a name="contact"></a>
<!-- CONTACT -->
## Kontakt
Mail: [mail@timokubera.it](mailto:mail@timokubera.it)

Project Link: [https://github.com/TimoKubera/IIRA](https://github.com/TimoKubera/IIRA)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 