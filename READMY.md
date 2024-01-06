
# Dane Autora 
 - imię i nazwisko: Marcin Polewski
 - e-mail: 01187274@pw.edu.pl
 - numer indeksu: 331 425 

# Cel i opis projektu 
 Celem projektu było utworzenie gry w statki w cyfrowej wersji, 
 bazując na wszystkim dobrze znanych zasadach. Owa gra ma kilka wersji, 
 realizowana tutaj to klasyczna - opisana na [wikipedi](https://en.wikipedia.org/wiki/Battleship_(game)), czyli:
 - uzytkownik po oddaniu strzalu komunikuje drugiemu hit, miss, albo sunk
 - plansza ma rozmar 10x10
 - konfiguracja statków to: 
    - jeden carrier o długości 5 pól 
    - jeden battleship o długości 4 pól
    - cztery cruiser-y o długości 3 pól
    - trzy patrol ship-y o długości dwóch pól

# Instrukcja gry
 Nalezy uruchomić main.py, co spowoduje odpalenie w nowym okienku gry. 
 Widoczne jest menu główne z trzeba guzikami:
  - Play PVP - rozpoczęcie gry w trybie Player vs Player
  - Play PVP - rozpoczęcie gry w trybie Player vs Computer
  - Exit Game - wyjście z gry
  
 Po wybraniu dowolnego trybu wyswietlają się dwie plansze i pasek statusu. 
 Plansza po lewej stronie jest klasycznie planszą odbecnego gracza (jest podpisana na pasku statusu),
 planasza po prawej jest planszą oponenta. Na pasku statusu wyświetla się status floty - ile statkow 
 danego typu grasz ma rozmieszczonych na planszy. Oznacza to, ze na poczatku wszystkie wartosci pokazue 0 dzielone 
 przez liczbe statkow danego typu jaka nalezy rozmiescic. Następnie gdy zestrzelimy jakis statek, to na pasku statusu
 liczba statkow danego typu zmniejszy sie o 1  

 ### Tryp PVP
 Jeśli został wybrany tryb player vs player, gre rozpoczyna Player1, pozycjonuje on swoje statki zgodznie ze specyfikacja
 podaną na pasku statusu. Robi to przez przyciśnięcie klawisza na polu gdzie ma się statek zacząć i puszczeniu na polu gdzie ma się skończyć.
 Jeśli uzytkownik nie ma takiego statku zostanie powiadomiony o tym przez prompt wyskakujący na środku ekranu, jeśli występuje kolicja stanie się 
 analogicznie. Jeśli nie ma przeszkód statek zostanie pomyślie postawiony. Po postawieniu statków na ekranie pojawi się przyciski "Switch user", po
 jego kliknięciu gra wejsie z "Blackscreen phase" - ekran na którym wyświetla się komunikat, zeby gracze zamienili się przy komputerze. Aby opuścić
 te faze naley nacisnąć mysz. Teraz kolejn gracz pozycjonuje analogicznie statki i jak to zrobi moze przystapic do atakowania przeciwnika. Strzela
 on do przeciwnika przez nacisniecie mysza na pole przykryte chmurą. Jeśli będzie chciał on zaatakować ponownie te samo pole zostanie o tym
 powiadomiony. Po wykonaniu ataku pojawi się guzik do zmiany gracza i następnie sytuacja jest analogiczna do momentu, gdy któryś z graczy wygra. 

 Wtedy gra przechodzi w faze wyniku, pojawia się nazwa gracza który wygrał oraz podstawowe statystyki: 
   - Czas gry 
   - Ilość rozegranych rund (gdzie runde definiuje się przez wykonanie przez któregoś z graczy strzału)
   - Procent segmentów statków wygranego gracza, który nie został trafiony 
 Na dole wyświetlają się dwa przyciski:
   - Main menu - powrót to menu startowego 
   - Exit Game - wyjście z gry

 ### Tryp PVC 
 Jeśli został wybrany tryb Player vs Computer gra funkcjonuje w identyczny sposób, tylko nie pojawia się guzik do zmiany graczy - dzieje się to automatycznie. 

 gre rozpoczyna gracz, pozycjonuje on swoje statki zgodznie ze specyfikacja
 podaną na pasku statusu. Robi to przez przyciśnięcie klawisza na polu gdzie ma się statek zacząć i puszczeniu na polu gdzie ma się skończyć.
 Jeśli uzytkownik nie ma takiego statku zostanie powiadomiony o tym przez prompt wyskakujący na środku ekranu, jeśli występuje kolicja stanie się 
 analogicznie. Jeśli nie ma przeszkód statek zostanie pomyślie postawiony. W momencie gdy gracz ustawi wszystkie statki, moze przejść do atakowania bota
 klikając myszką w plansze oponenta. Powinien strzelać w pola przykrytę chmurą - jeszcze nie zaatkaowane. W przypadku gdy zaatakuje pole, 
 ponownie, zostanie o tym powiadomiony i gra da mu drugą szanse. Gra się toczy do momentu, kiedy któryś z gracz nie zostanie pokonany.

 Wtedy gra przechodzi w faze wyniku, pojawia się nazwa gracza który wygrał oraz podstawowe statystyki: 
   - Czas gry 
   - Ilość rozegranych rund (gdzie runde definiuje się przez wykonanie przez któregoś z graczy strzału)
   - Procent segmentów statków wygranego gracza, który nie został trafiony 
 Na dole wyświetlają się dwa przyciski:
   - Main menu - powrót to menu startowego 
   - Exit Game - wyjście z gry

# Podział na klasy 
(tabulacja oznacza dziedziczenie)

### Warstwa dostępu do danych 
 - AssetLoader - klasa wczytuje z plików wszystkie zasoby, a następnie udostępnia je jako atrybuty publiczne 
### Warstwa obsługi uzytkowniak 
 - UIObject - klasa będąca postawą wszystkich klas odpowiedzialnych za wyświetalanie
    - ScreenVisualizer - klasa wyświtlająca elementy niedynamiczne (tło, logo, prompt do zmiany graczy)
    - StatusBarVisualizer - klasa wyświetlająca pasek statusu dla uzytkownika
    - PromptVisualizer - klasa odpowiedzialna za wyświetlanie wszystkich promptów dla uzytkownika 
    - GameBoardVisualizer - klasa odpowiedzialna za wyświetlanie planszy graczy 
 - Prompt - klasa odpowiedzialna za obsługę pojedynczego prompta i jego wyświetlanie
 - InputHandler - klasa odpowiedzialna za obsługę wejścia uzytkownika. Składa się z głównej metody 
                  mouse_button_interaction, która wywołuje inne metody tej klasy, które sprawdzają czy dana 
                  interakcja została wykonana, jeśli tak wywołują odpowiednią funkcje w kontrolerze gry
                  (GameLogicController) i zwracają prawdę, zeby nie trzeba było sprawdzać innych interakcji 
 - Button - klasa bazowa dla innych guzików, ma metody odpowiedzialne za wyswietlanie i sprawdzanie czy 
            guzik jest wcisnięty 
    - PlayPVPButton - guzik wyboru trybu(Player vs Player)
    - PlayPVCButton - guzik wyboru trybu (Player vs Computer)
    - ExitStartScreenButton - guzik wyjścia z gry wyświetlany na ekranie głównym 
    - ExitEndScreenButton - guzik wyjścia z gry wyświetlany na końcowym ekranie 
    - MainMenuButton - guzik powrotu do menu głównego
    - SwitchUserButton - guzik do aktualnego gracza wyswietlany po wykonaniu mozliwych ruchow
 - ButtonHandler - klasa odpowiedzialna za rysowanie guzikow na ekranie i patrzenie czy zostały wciśnięte
 - ImageHanlder - korzysta z klasy AssetLoader, zwraca kopie wczytanych elementow jesli to konieczne,
                  ma funkcjonalność generowania statycznych elementów(logo, prompt do zmiany uzytkownika, "alias" wygranego)
                  lub tez generowania obrazkow z tekstu, zaleznie od przeznacznia(automatycznie dobiera kolor,
                  czcionkę i jej wielkość). Ma tez kilka metod do wyliczania współrzędnych w taki sposób, 
                  aby umieszczając obraz w obrazie mozna było go centrować w określony sposób
### Warstwa obsługująca logikę
 - Ship - klasa reprezentuje pojedynczy statek na planszy, będąca podstawą dla klas dziedicznych(jedyne co, to mają one 
          odrazu przypisane długości). Klasa ma funkcjonalność pozwalającą liczyć ile segmentów statku zostało zaatakowanych, 
          czy został zestrzelony
    - Carrier
    - Battleship
    - Cruiser 
    - PatrolShip
 - BoardCell - klasa reprezentuje jedno pole na planczy gry, jej funkcjonalność pozwala na przyjęcie ataku, sprawdzenie czy jest na     
               niej statek, sprawdzenie czy pole zostało zaatakowane itd
 - Player - klasa gracza, główna jej funkcjonalnośc skupia się wokół przetrzymywanej listy dwuwymiarowej z BoardCell-i tworzących 
            plansze do gry. Ma metody obsługujące ustawianie statku(jeśli się nie da zostanie wyrzucony błąd), za przyjmowanie ataku
            i jego przeprowadzanie 
    - BotPlayer - rozszrza funkcjonalność klasy Player o automatyzacje strzelania i ustaiwania statków

 ### Błędy
  - OcupiedCellError - wyrzucone jeśli prubuje się postawić statek na polu, gdzie juz jakis inny stoi 
  - CellAlreadyShotError - wyrzucony jesli gracz próbuje zaatakować to samo pole drugi raz 
  - ShipPlacingError - wyrzucony jeśli nie mozemy ustawić w danym miejscu statku, ze względu na kolizje 
                        lub nie mieści się na planszy 
  - NotSuchShipToPlaceError - wyrzucony, jeśli uzytkownik prubuje postawić statek, którego nie ma
  - OutOfTableError - wyrzucony jeśli kolumna lub rząd nie występują w tabeli

# Część refleksyjna

### Czego nie udało się zrealizować:
 - Instrukcja co nalezy teraz zrobić, wyświetlana na pasku statusu - nie udało się tego zrealizować, gdyz nie bylo juz miejsca na pasku,
 uwazam ze jego obecna forma wizualna jest ładniejsza, a takie instrukcie przydają się tylko gdy gracz uczy się obsługi - 
 moze przeczytać intrukcje. Zawiodło planowanie..
 - animacje ataku - pierwotnie zamierzałem to zrealizować, ale w późniejszych etapach projektu doszedłem do wniosku ze wole skupic 
 sie na funkcjonalnych aspektach, jak dodawanie menu, statystyk itp 
 - Czas jak długo prompt miałby wyświetlać się na ekranie miał zalezeć od długości tekstu, ale przyjenty cooldown tak dobrze realizuje te funckjonalność, 
 nie chicałem psuć tego co działa

### Co się zmieniło od pierwotnych załozeń:
 - Pierwotnie wizualicacja gry miala odbywac się przez dzieciczenie obiektów wyswietlajacych po obiektach odpowiedzialnych za logike,
 po przemysleniach stwierdzilem, ze bedzie to mniej czytelne i trudniejsze w wykonaniu 
 - Pierwotnie tryp PVP, ekran startowy i koncowy, i prompty nie byly planowane 
 - Klasa ImageHandler miała generować wszytkie obrazy, aby trochę zaprać funkjonalności z innych klas UI, ale ostatecznie stwierdziłem
 ze efekt byłby odwrotny i zamiast lepszej seraracji uzyskałbym zwalenie wszystkiego do jednej klasy(generowanie obrazów to znaczna część kod w UI)
 ###

### Wnioski po wykonaniu: 
 - Warto przed zaczęciem dokonać analizy, zaplanować sobie dokładnie klasy, przemyslec wszystkie etapy projektu. Zacząłem projekt realizować 
 trochę jak takie proste zadanie do filmiku na laby, chwile przemyślałe i zacząłem pisać. Miałem koncepcje w głowie, ale jakieś utrwalenie tego, 
 przepmyślenie dalszych kroków byłoby pomocne
- Trzeba wypracować system monitorowanie progresu na projekcie, to znaczy co jest aktualnie robione, co do zrobienia itp. Bez tego człowiek się trochę gubi
- Robić backupy od samego początku! Projekt zacząłem robić w lokalnym repozytorium i po wykonaniu juz sporego kawalka roboty chcialem wrzucić to na serwer.
  niestety coś nie poszło (sprytny student stwierdził ze godzina 24 to jest świetny moment na coś takiego) i wszystkie commity znikneły. 
  Nie miałem zadnego backup tej pracy