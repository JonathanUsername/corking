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
    var GAME_WIDTH = 600;
    var GAME_HEIGHT = 500;
    var TURN = 0;
    var map,
        layer,
        marker,
        currentTile,
        cursors,
        game,
        Buildings,
        savedLayerOnEndTurn,
        loadedLayer,
        loaded_game = false;



    function stripCircular() {
        var obj = []
        for (var i in mapdata) {
            for (var j in mapdata[i]) {
                // Get rid of circular properties
                savedLayerOnEndTurn = mapdata[i][j].layer;
                mapdata[i][j].layer = null;
                mapdata[i][j].collisionCallbackContext = null;
                obj.push(mapdata[i][j])
            }
        }
        return obj
    }

    get_new_game = function() {
        $.get("/newgame", function(data) {
            loaded_game = data;
            console.log(JSON.stringify(data))
            try {
                game.destroy()
                console.log("Loading new game")
            } catch (e) {
                console.log("Game starting")
            }
            start_game(data)
        })
    }

    get_new_game();



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
            TURN = data.turn
                //debugger
            game.load.tilemap('desert', url, data, Phaser.Tilemap.TILED_JSON);
            game.load.tilemap('buildings', 'data/buildings.json', null, Phaser.Tilemap.TILED_JSON);
            game.load.image('tiles', 'tmw_desert_spacing.png');
        }

        function create() {
            map = game.add.tilemap('desert');
            buildings = game.add.tilemap('buildings');
            desert = buildings.getTile(0, 0);
            map.addTilesetImage('Desert', 'tiles');
            currentTile = map.getTile(17, 16);
            CurrentMap = map.createLayer('Ground');
            CurrentMap.resizeWorld();
            // Buildings = map.createBlankLayer("Buildings");
            // console.log(Buildings)
            BUILDING_INFO = {
                "solar_panel": {
                    tile: buildings.getTile(1, 0),
                    power_cost: 30
                },
                "residence": {
                    tile: buildings.getTile(2, 0),
                    power_cost: 40
                }
            }
            BUILDING_TILES = [22,23];
            marker = game.add.graphics();
            marker.lineStyle(2, 0x000000, 1);
            marker.drawRect(0, 0, 32, 32);
            cursors = game.input.keyboard.createCursorKeys();
            restart_key = game.input.keyboard.addKey(Phaser.Keyboard.Q);
            restart_key.onDown.add(function() {
                get_new_game();
            }, this);
            end_turn_key = game.input.keyboard.addKey(Phaser.Keyboard.E);
            end_turn_key.onDown.add(function() {
                mapdata = map.layers[0].data
                end_turn(mapdata);
            }, this);
            debug_key = game.input.keyboard.addKey(Phaser.Keyboard.A);
            debug_key.onDown.add(function() {
                GAME_WIDTH = 1200;
                GAME_HEIGHT = 1200;
                get_new_game();
            }, this);
            game.camera.x = 800 / 2; // Change this to what the maximum array size is in loaded data
            game.camera.y = 800 / 2;

            HUD = new HUDvm();
            ko.applyBindings(HUD);
        }

        function update() {
            marker.x = CurrentMap.getTileX(game.input.activePointer.worldX) * 32;
            marker.y = CurrentMap.getTileY(game.input.activePointer.worldY) * 32;
            if (game.input.mousePointer.isDown) {
                // Within Buildings, not the ground layer
                console.log(CurrentMap)
                var xt = CurrentMap.getTileX(marker.x)
                var yt = CurrentMap.getTileY(marker.y)
                currentTile = map.getTile(xt, yt, CurrentMap);
                if (BUILDING_TILES.indexOf(currentTile.index) != -1) {
                    marker.lineStyle(2, 0xffffff, 1);
                    console.log("You can't build on that! There's already a building there!")
                } else {
                    if (game.input.keyboard.isDown(Phaser.Keyboard.S)) {
                        placeBuilding(xt, yt, currentTile, CurrentMap, "solar_panel")
                    } else if (game.input.keyboard.isDown(Phaser.Keyboard.R)) {
                        placeBuilding(xt, yt, currentTile, CurrentMap, "residence")
                    } else {
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

        function placeBuilding(x, y, tile, layer, building) {
            var cost = BUILDING_INFO[building]["power_cost"]
            var b_tile = BUILDING_INFO[building]["tile"]
            if (cost <= HUD.solar_power()) {
                map.putTile(b_tile, x, y, layer);
                tile.properties.built = true;
                HUD.solar_power(HUD.solar_power() - cost);
            } else {
                console.log("NOT ENOUGH POWER")
            }
        }


        function end_turn(mapdata) {
            obj = {};
            obj.map = [];
            for (var i in mapdata) {
                for (var j in mapdata[i]) {
                    obj.map.push(mapdata[i][j].index)
                }
            }
            obj.turn = TURN;
            obj.solar_power = HUD.solar_power();
            var jsonSave = JSON.stringify(obj, null, '\t');
            $.ajax({
                url: "/endturn",
                type: "POST",
                contentType: 'application/json;charset=UTF-8',
                data: jsonSave,
                success: function(data) {
                    json = JSON.parse(data)
                    loadedLayer = json.map;
                    HUD.solar_power(json.solar_power)
                    console.log("Loading new game")
                }
            })
        }

        function render() {
            game.debug.text('Q = Restart\nR = Residence\nS = Solar', 32, 32, '#efefef');
        }

        // use this for all resources or turns or anything that needs to bind to the view
        // it is a global variable called HUD
        function HUDvm (){
            var self = this;
            self.solar_power = ko.observable(100);
        }


    }
});