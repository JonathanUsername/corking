
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

    munch = function() {
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
            console.log(url)
            console.log(data)
            //debugger
            game.load.tilemap('desert', url, data, Phaser.Tilemap.TILED_JSON);
            game.load.image('tiles', 'tmw_desert_spacing.png');
        }

        function create() {
            map = game.add.tilemap('desert');
            map.addTilesetImage('Desert', 'tiles');
            currentTile = map.getTile(17, 16);
            layer = map.createLayer('Ground');
            layer.resizeWorld();
            marker = game.add.graphics();
            marker.lineStyle(2, 0x000000, 1);
            marker.drawRect(0, 0, 32, 32);
            cursors = game.input.keyboard.createCursorKeys();
            restart_key = game.input.keyboard.addKey(Phaser.Keyboard.R);
            restart_key.onDown.add(function(){
                munch();
            }, this);
        }

        function update() {
            marker.x = layer.getTileX(game.input.activePointer.worldX) * 32;
            marker.y = layer.getTileY(game.input.activePointer.worldY) * 32;
            if (game.input.mousePointer.isDown) {
                if (game.input.keyboard.isDown(Phaser.Keyboard.SHIFT)) {
                    currentTile = map.getTile(layer.getTileX(marker.x), layer.getTileY(marker.y));
                    console.log(currentTile)
                } else {
                    if (map.getTile(layer.getTileX(marker.x), layer.getTileY(marker.y)) != currentTile) {
                        map.putTile(currentTile, layer.getTileX(marker.x), layer.getTileY(marker.y))
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

        function render() {
            game.debug.text('Left-click to paint. Shift + Left-click to select tile. Arrows to scroll.', 32, 32, '#efefef');
        }

        munch()
    }
});
