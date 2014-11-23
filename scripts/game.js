
requirejs.config({
    baseUrl: 'scripts',
    paths: {
        Phaser: 'phaser',
        jquery: 'jquery'
    },
});

require(['Phaser', 'jquery'], function(Phaser, $) {
    app = {}
    var GAME_WIDTH = 400;
    var GAME_HEIGHT = 500;
    var map,
    layer,
    marker,
    currentTile,
    cursors,
    game,
    loaded_game = false;

    get_new_game = function() {
        $.get("/newgame", function(data){
            loaded_game = data;
            console.log(JSON.stringify(data))
            try {
                game.destroy()
                console.log("Loading new game")
            }
            catch(e) {
                console.log("Game starting")
            }
            start_game(data)
        })
    }

    get_new_game();

    end_turn = function(mapdata){
        var obj = []
        for (var i in mapdata){
            for (var j in mapdata[i]){
                // Get rid of circular properties
                mapdata[i][j].layer = null
                mapdata[i][j].collisionCallbackContext = null
                obj.push(mapdata[i][j])
            }
        }
        var jsonSave = JSON.stringify(obj)
        $.ajax({
            url: "/endturn",
            type: "POST",
            data: jsonSave,
            success: function(data){
                loaded_game = data;
                console.log(JSON.stringify(data))
                try {
                    game.destroy()
                    console.log("Loading new game")
                }
                catch(e) {
                    console.log("Game starting")
                }
                start_game(data)
            }
        })
    }

    start_game = function(loaded){
        game = new Phaser.Game(GAME_WIDTH, GAME_HEIGHT, Phaser.AUTO, '', {
            preload: preload,
            create: create,
            update: update,
            render: render
        });

        function preload() {
            var url = (loaded) ? null : 'data/desert.json';
            var data = loaded || null;
            //debugger
            game.load.tilemap('desert', url, data, Phaser.Tilemap.TILED_JSON);
            game.load.tilemap('buildings', 'data/buildings.json', null, Phaser.Tilemap.TILED_JSON);
            game.load.image('tiles', 'tmw_desert_spacing.png');
        }

        function create() {
            map = game.add.tilemap('desert');
            buildings = game.add.tilemap('buildings');
            desert = buildings.getTile(0, 0);
            solar_panel = buildings.getTile(1, 0);
            residence = buildings.getTile(2, 0);
            map.addTilesetImage('Desert', 'tiles');
            currentTile = map.getTile(17, 16);
            layer = map.createLayer('Ground');
            layer.resizeWorld();
            marker = game.add.graphics();
            marker.lineStyle(2, 0x000000, 1);
            marker.drawRect(0, 0, 32, 32);
            cursors = game.input.keyboard.createCursorKeys();
            restart_key = game.input.keyboard.addKey(Phaser.Keyboard.Q);
            restart_key.onDown.add(function(){
                get_new_game();
            }, this);
            end_turn_key = game.input.keyboard.addKey(Phaser.Keyboard.E);
            end_turn_key.onDown.add(function(){
                mapdata = map.layers[0].data
                end_turn(mapdata);
            }, this);
        }

        function update() {
            marker.x = layer.getTileX(game.input.activePointer.worldX) * 32;
            marker.y = layer.getTileY(game.input.activePointer.worldY) * 32;
            if (game.input.mousePointer.isDown) {
                var xt = layer.getTileX(marker.x)
                var yt = layer.getTileY(marker.y)
                currentTile = map.getTile(xt, yt);
                console.log(currentTile)
                if (!currentTile.properties.built){
                    // Holding shift
                    if (game.input.keyboard.isDown(Phaser.Keyboard.S)) {
                        console.log("painting solar")
                        map.putTile(solar_panel, xt, yt)
                        currentTile.properties.built = true;
                        // currentTile = map.getTile(xt, yt);
                        // console.log(currentTile)
                    } else if (game.input.keyboard.isDown(Phaser.Keyboard.R)) {
                        console.log("painting residence")
                        map.putTile(residence, xt, yt)
                        currentTile.properties.built = true;
                        // currentTile = map.getTile(xt, yt);
                        // console.log(currentTile)
                    } else {
                        // Just clicking
                        map.putTile(desert, xt, yt)
                        // if (map.getTile(xt, yt) != currentTile) {
                        //     map.putTile(currentTile, layer.getTileX(marker.x), layer.getTileY(marker.y))
                        // }
                    }
                } else {
                    marker.lineStyle(2, 0xffffff, 1);
                    console.log("You can't build on that! There's already a building there!")
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

        function render() {
            game.debug.text('Q = Restart\nR = Residence\nS = Solar', 32, 32, '#efefef');
        }


    }
});
