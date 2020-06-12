// hiding all the loaders UI when loading the website.
// loader UI --> presentation of loading circle when calling ajax request.
hide_all_loaders();

// Connecting html chart elements to JS
var england_ctx = document.getElementById("England_chart").getContext('2d');
var spain_ctx = document.getElementById("Spain_chart").getContext('2d');
var italy_ctx = document.getElementById("Italy_chart").getContext('2d');
var germany_ctx = document.getElementById("Germany_chart").getContext('2d');

// Loaders UI spinner for each league prediction
plLoaderValue =  'plRing';
bbvaLoaderValue =  'bbvaRing';
serieALoaderValue =  'serieARing';
bundesLeagueLoaderValue =  'bundesLeaugeRing';



// Initialization values for charts
init_data =  [1,2,1];

// Creating charts for each league
PL_Chart = createChart(england_ctx);
BBVA_Chart = createChart(spain_ctx);
SERIE_A_Chart = createChart(italy_ctx);
BUNDESLIGA_Chart = createChart(germany_ctx);


// connecting html buttons to their relevant handlers
document.getElementById("England_btn").addEventListener("click", PL_call);
document.getElementById("Spain_btn").addEventListener("click", BBVA_call);
document.getElementById("Italy_btn").addEventListener("click", SERIE_A_call);
document.getElementById("Germany_btn").addEventListener("click", BUNDESLIGA_call);



// English Premier league button handler
function PL_call(){

    e_home = document.getElementById("PL_H");
    home_team = e_home.options[e_home.selectedIndex].text;
    e_away = document.getElementById("PL_A");
    away_team = e_away.options[e_away.selectedIndex].text;
    console.log(home_team);
    console.log(away_team);

    valid = validation_teams_name(home_team,away_team)

    if(valid){
        new_url = 'http://127.0.0.1:5000/predict/England/'+ home_team +'/' + away_team;
        ajax_call(new_url,PL_Chart,plLoaderValue);
    }
}

// Spanish La liga button handler
function BBVA_call(){
    e_home = document.getElementById("BBVA_H");
    home_team = e_home.options[e_home.selectedIndex].text;
    e_away = document.getElementById("BBVA_A");
    away_team = e_away.options[e_away.selectedIndex].text;
    console.log(home_team);
    console.log(away_team);

    valid = validation_teams_name(home_team,away_team)

    if(valid){
        new_url = 'http://127.0.0.1:5000/predict/Spain/'+ home_team +'/' + away_team;
        ajax_call(new_url,BBVA_Chart,bbvaLoaderValue);
    }
}

// Italian Serie A button handler
function SERIE_A_call() {
    e_home = document.getElementById("SERIE_H");
    home_team = e_home.options[e_home.selectedIndex].text;
    e_away = document.getElementById("SERIE_A");
    away_team = e_away.options[e_away.selectedIndex].text;

    valid = validation_teams_name(home_team,away_team)

    if(valid){
        new_url = 'http://127.0.0.1:5000/predict/Italy/'+ home_team +'/' + away_team;
        ajax_call(new_url,SERIE_A_Chart,serieALoaderValue);
    }
}

// Germany BundesLiga button handler
function BUNDESLIGA_call() {
    e_home = document.getElementById("BUNDESLIGA_H");
    home_team = e_home.options[e_home.selectedIndex].text;
    e_away = document.getElementById("BUNDESLIGA_A");
    away_team = e_away.options[e_away.selectedIndex].text;

    console.log(home_team);
    console.log(away_team);

    valid = validation_teams_name(home_team,away_team);

    if(valid){
        new_url = 'http://127.0.0.1:5000/predict/Germany/'+ home_team +'/' + away_team;
        ajax_call(new_url,BUNDESLIGA_Chart,bundesLeagueLoaderValue);
    }
}

// generic Ajax call for updating Chart, callback --> return JSON ['HomeTeam': 'x' , 'Draw': 'y' , 'AwayTeam' 'z']  (x + y + z) = 1
function ajax_call(url_call,chart,loader_value) {
    show_loaders(loader_value);
    $.ajax({
        xhrFields: {
            withCredentials: false
        },
        type: "GET",
        url: url_call,
        crossDomain: true,
    }).done(function (data) {


        console.log(data);

        // Normalization (as mention above --> x + y + z = 1
        sum  = data.HomeTeam + data.Draw + data.AwayTeam;
        data.HomeTeam = data.HomeTeam / sum;
        data.Draw = data.Draw / sum;
        data.AwayTeam = data.AwayTeam / sum;

        new_data = [data.HomeTeam,data.Draw,data.AwayTeam];
        hide_loaders(loader_value);
        drawData(chart,new_data);
    },);
}

// checking whether the home team and away team was chosen properly
function validation_teams_name(home_team, away_team){
    valid = true;
    if((home_team === away_team)){
        valid = false
        swal("Select different teams.","","error")
    }
    else if(home_team.trim() === "Home Team" && away_team.trim() === "Away Team"){
        valid = false
        swal("Select home and away teams.", "","error")
    }
    else if(home_team.trim()=== "Home Team"){
        valid = false
        swal("Select home team.","","error")
    }
    else if(away_team.trim() === "Away Team"){
        valid  = false
        swal("Select away team.","","error")
    }
    return valid;
}

// drawing the json from the ajax callback to the relevant chart
function drawData(chart_Listener,predicate) {
     newChart =  redrawChart(chart_Listener,predicate);

    chart_Listener = newChart;
    chart_Listener.update();
}

function redrawChart(chart_Listener, predicate){
    return new Chart(chart_Listener, {
        type: 'pie',
        data: {
            labels: ["HomeTeam", "Draw", "AwayTeam"],
            datasets: [{
                backgroundColor: [
                    "#34bc5d",
                    "#db4856",
                    "#1b8ca6",
                ],
                data : predicate
            }]
        },
        options:{
            legend: {
                labels: {
                    fontColor: "white",
                    fontSize: 20
                }
            }
        }
    });
}

function createChart(ctx){
    return new Chart(ctx,{
        type: 'pie',
        data: {
            labels: ["HomeTeam", "Draw", "AwayTeam"],
            datasets: [{
                backgroundColor: [
                    "#34bc5d",
                    "#db4856",
                    "#1b8ca6",
                ],
                data: init_data  // init_data = [1 , 2 , 1];
            }]
        },
        options:{
            legend: {
                labels: {
                    fontColor: "white",
                    fontSize: 20
                }
            }
        }
    });
}

function hide_loaders(value) {
    document.getElementById(value).style.display = "none";
}

function show_loaders(value){
    document.getElementById(value).style.display = "initial";
}

function hide_all_loaders(){
    document.getElementById('plRing').style.display = "none";
    document.getElementById('bbvaRing').style.display = "none";
    document.getElementById('serieARing').style.display = "none";
    document.getElementById('bundesLeaugeRing').style.display = "none";
}

