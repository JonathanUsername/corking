requirejs.config({
    baseUrl: 'scripts',
    paths: {
        Phaser: 'phaser',
        jquery: 'jquery',
        knockout: 'knockout'
    },
});

require(['Phaser', 'jquery', 'knockout'], function(Phaser, $, ko) {
    app = {}
    var GAME_WIDTH = window.innerWidth;
    var GAME_HEIGHT = 500;
    var TURN = 0;
    var layer,
        //marker,
        currentTile,
        GAME_ID,
        cursors,
        //game,
        Buildings,
        BUILDING_TILES,
        BUILDING_INFO,
        savedLayerOnEndTurn,
        loadedLayer,
        loaded_game = false;



    // function stripCircular() {
    //     var obj = []
    //     for (var i in mapdata) {
    //         for (var j in mapdata[i]) {
    //             // Get rid of circular properties
    //             savedLayerOnEndTurn = mapdata[i][j].layer;
    //             mapdata[i][j].layer = null;
    //             mapdata[i][j].collisionCallbackContext = null;
    //             obj.push(mapdata[i][j])
    //         }
    //     }
    //     return obj
    // }

    get_new_game = function() {
        $.get("/newgame", function(data) {
            loaded_game = data;
            try {
                game.destroy()
                console.log("Loading new game")
            } catch (e) {
                console.log("Game starting")
            }
            start_game(data)
        })
    }

    $(".new_game.button").click(function(){
        $(".intro").hide()
        get_new_game()
    });

    start_game = function(loaded) {
        game = new Phaser.Game(GAME_WIDTH, GAME_HEIGHT, Phaser.AUTO, 'game_box', {
            preload: preload,
            create: create,
            update: update,
            render: render
        });

        function preload() {
            var url = (loaded) ? null : 'data/desert.json';
            var data = loaded || null;
            // TURN = data.turns
            // GAME_ID = data.game_id
            console.log(GAME_ID)
                //debugger
            game.load.tilemap('desert', url, data, Phaser.Tilemap.TILED_JSON);
            game.load.tilemap('buildings', 'data/buildings.json', null, Phaser.Tilemap.TILED_JSON);
            game.load.image('tiles', 'tmw_desert_spacing.png');
            // Need ogg for FF
            game.load.audio('eno', ['data/audio/brian-eno-signals.mp3', 'data/audio/brian-eno-signals.ogg']);
        }

        function create() {
            map = game.add.tilemap('desert');
            buildings = game.add.tilemap('buildings');
            t_desert = buildings.getTile(0, 0);
            t_solar = buildings.getTile(1, 0);
            t_residence = buildings.getTile(2, 0);
            t_fog = buildings.getTile(3,0)
            map.addTilesetImage('Desert', 'tiles');
            currentTile = map.getTile(17, 16);
            CurrentMap = map.createLayer('Ground');
            CurrentMap.resizeWorld();
            FogMap = map.createLayer('Fog');
            // console.log(Buildings)
            BUILDING_INFO = {   
                "solar_panel": {
                    index: 22,
                    tile: buildings.getTile(1, 0),
                    power_cost: 30,
                    name: "Solar Panels",
                    available: true,
                    key: "solar_panel"
                },
                "residence": {
                    index: 23,
                    tile: buildings.getTile(2, 0),
                    power_cost: 40,
                    name: "Residential Pod",
                    available: true,
                    key: "residence"
                }
            }
            BUILDING_TILES = [22,23];
            marker = game.add.graphics();
            marker.lineStyle(2, 0x000000, 1);
            marker.drawRect(0, 0, 32, 32);
            cursors = game.input.keyboard.createCursorKeys();

            // debug_key = game.input.keyboard.addKey(Phaser.Keyboard.A);
            // debug_key.onDown.add(function() {
            //     GAME_WIDTH = 1200;
            //     GAME_HEIGHT = 1200;
            //     get_new_game();
            // }, this);

            game.camera.x = 800 / 2; // Change this to what the maximum array size is in loaded data
            game.camera.y = 800 / 2;

            music = game.add.audio('eno');
            // music.play();  it gets annoying
            music.loop = true;

            HUD = new HUDvm();
            ko.applyBindings(HUD);

            clearfog()
        }

        function update() {
            marker.x = CurrentMap.getTileX(game.input.activePointer.worldX) * 32;
            marker.y = CurrentMap.getTileY(game.input.activePointer.worldY) * 32;
            var xt = CurrentMap.getTileX(marker.x)
            var yt = CurrentMap.getTileY(marker.y)
            if (HUD.selected_building() != false){
                
            }
            if (game.input.mousePointer.isDown) {
                // Within Buildings, not the ground layer
                currentTile = map.getTile(xt, yt, CurrentMap);
                if (BUILDING_TILES.indexOf(currentTile.index) != -1) {
                    marker.lineStyle(2, 0xffffff, 1);
                    console.log("You can't build on that! There's already a building there!")
                } else {
                    if (HUD.selected_building() != false) {
                        if (HUD.selected_building() == "sell"){
                            console.log("Write selling code")
                        } else {
                            placeBuilding(xt, yt, currentTile, CurrentMap)
                        }
                    } else {
                        // var newtile = (map.getTile(xt,yt,FogMap))
                        // newtile.alpha = 0
                        // map.putTile(newtile,xt,yt,FogMap)
                        console.log(currentTile)
                    }
                }
            }

            if (cursors.left.isDown) {
                game.camera.x -= 4;
            } else if (cursors.right.isDown) {
                game.camera.x += 4;
            }

            if (cursors.up.isDown) {
                game.camera.y -= 4;
            } else if (cursors.down.isDown) {
                game.camera.y += 4;
            }
        }

        function placeBuilding(x, y, tile, layer) {
            var cost = BUILDING_INFO[HUD.selected_building()]["power_cost"]
            var b_tile =  BUILDING_INFO[HUD.selected_building()]['tile']
            if (cost <= HUD.solar_power()) {
                map.putTile(b_tile, x, y, layer);
                HUD.solar_power(HUD.solar_power() - cost);
            } else {
                console.log("NOT ENOUGH POWER")
            }
            clearfog();
        }

        findBuildings = function(){
            var arr = []
            // Y FIRST ???? FFS!!!!
            for (var y in map.layer.data){
                for (var x in map.layer.data[y]){
                    // if its index is in BUILDING_TILES then it's a building, this finds non-desert for now
                    map.layer.data[y][x].index != 30 ? arr.push({"x":x,"y":y}) : false
                }
            }
            return arr
        }

        getAdjacent = function(tile, radius, layer){
            var radius = radius || 1;
            var arr = [
                map.getTile(tile.x+1,tile.y+1,layer),
                map.getTile(tile.x+1,tile.y,layer),
                map.getTile(tile.x,tile.y+1,layer),
                map.getTile(tile.x-1,tile.y-1,layer),
                map.getTile(tile.x-1,tile.y,layer),
                map.getTile(tile.x,tile.y-1,layer),
                map.getTile(tile.x+1,tile.y-1,layer),
                map.getTile(tile.x-1,tile.y+1,layer)
            ]
            return arr;
        }

        clearfog = function(){
            var buildings = findBuildings();
            for (var i in buildings){
                var f_tile = map.getTile(buildings[i].x, buildings[i].y, FogMap)
                f_tile.alpha = 0;
                map.putTile(f_tile,buildings[i].x,buildings[i].y,FogMap)
                var adj = getAdjacent(f_tile,1,FogMap);
                for (var i in adj){
                    adj[i].alpha = 0;
                }
            }
        }

        function MapTile(index, properties){
            var self = this;
            self.index = index;
            self.properties = properties;
        }

        function end_turn() {
            HUD.lock(true);
            mapdata = CurrentMap.layer.data // eventually should be for all layers
            obj = {};
            obj.map = [];
            for (var i in mapdata) {
                for (var j in mapdata[i]) {
                    obj.map.push(new MapTile(mapdata[i][j].index, mapdata[i][j].properties))
                }
            }
            obj.turn = TURN;
            obj.solar_power = HUD.solar_power();
            obj.population = HUD.population();
            obj.max_population = HUD.max_population();
            obj.happiness = HUD.happiness();
            var jsonSave = JSON.stringify(obj, null, '\t');
            $.ajax({
                url: "/endturn",
                type: "POST",
                contentType: 'application/json;charset=UTF-8',
                data: jsonSave,
                success: function(data) {
                    json = JSON.parse(data)
                    loadedLayer = json.map;
                    updateMap(json.map)
                    HUD.solar_power(json.solar_power)
                    HUD.population(json.population)
                    HUD.max_population(json.max_population)
                    HUD.happiness(json.happiness)
                    HUD.newspaper(json.newspaper)
                    console.log("Loading new game")
                    HUD.lock(false)
                }
            })
        }

        function render() {
            game.debug.text('Q = Restart | R = Residence | S = Solar | E = End Turn', 32, 32, '#efefef');
        }


        // There must be a better way to do this...
        // I'm mapping the single array passed by the backend, to the array of 
        // arrays that phaser uses. Each 2nd dimension array has length 40.
        function updateMap(new_map){
            var count = 0
            for (var i in CurrentMap.layer.data){
                for (var j in CurrentMap.layer.data[i]){
                    var tile = CurrentMap.layer.data[i][j]
                    tile.index = new_map[count].index
                    tile.properties = new_map[count].properties
                    if (tile.properties.rioting){
                        tile.index = 38
                    }
                    count++
                }
            }
            // this is simply to interact with the map and trigger an update
            map.replace(0,0) 
            clearfog();
        }

        // use this for all resources or turns or anything that needs to bind to the view
        // it is a global variable called HUD, at the moment it doesn't compute anything
        // since we leave all that to the backend. This means max pop won't update til 
        // turn end, for instance.. 
        function HUDvm (){
            var self = this;
            self.lock = ko.observable(false);
            self.solar_power = ko.observable(100);
            self.population = ko.observable(4);
            self.max_population = ko.observable(8);
            self.overpopulated = ko.computed(function(){
                return self.population() > self.max_population() ? true : false
            })
            self.happiness = ko.observable(100)
            self.face = ko.computed(function(){
                if (self.happiness() >= 75){
                    return '<i class="icon-emo-grin"></i>'
                } else if (self.happiness() < 75 && self.happiness() >= 50){
                    return '<i class="icon-emo-happy"></i>'
                } else if (self.happiness() < 50 && self.happiness() > 25) {
                    return '<i class="icon-emo-unhappy"></i>'
                } else if (self.happiness() <= 25 && self.happiness() > 0){
                    return '<i class="icon-emo-angry"></i>'
                } else if (self.happiness() == 0){
                    return '<i class="icon-emo-shoot"></i>'
                }
            })
            self.building_info = ko.observable(BUILDING_INFO)
            self.buildings = ko.observableArray()
            for (var i in self.building_info()){
                self.buildings.push(new MenuItem(BUILDING_INFO[i]))
            }
            self.selected_building = ko.observable(false);
            self.menu_choice = ko.observable('buildings');
            self.music_toggle = function(){
                if (music.isPlaying){
                    music.stop()
                    self.music_on(false)
                } else{
                    music.play()
                    self.music_on(true)
                } 
            }
            self.music_on = ko.observable(false)
            self.choose_newspaper = function(){
                self.menu_choice('newspaper')
            }
            self.choose_buildings = function(){
                self.menu_choice('buildings')
            }
            self.select_sell = function(){
                self.selected_building("sell")
            }
            self.end_turn = function(){
                end_turn();
            }
            self.newspaper = ko.observableArray()
        }

        function MenuItem(info){
            var self = this
            self.name = ko.observable(info.name)
            self.key = ko.observable(info.key)
            self.power_cost = ko.observable(info.power_cost)
            self.index = ko.observable(info.index)
            self.available = ko.observable(info.available)
            self.tile = ko.observable(info.tile)
            self.change_selected_building = function(){
                HUD.selected_building(self.key())
            }
        }

    }
});