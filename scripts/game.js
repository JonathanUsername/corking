var app = {}

requirejs.config({
    baseUrl: 'scripts',
    paths: {
        Phaser: 'phaser',
        jquery: 'jquery'
    },
});

require(['Phaser', 'jquery'], function(Phaser, $) {
    var GAME_WIDTH = 400;
    var GAME_HEIGHT = 400;

    console.log($)

    var game = new Phaser.Game(GAME_WIDTH, GAME_HEIGHT, Phaser.CANVAS, 'game-box', {
        preload: preload,
        create: create,
        update: update,
        render: render
    });

    function preload() {

        game.load.tilemap('desert', 'data/desert.json', null, Phaser.Tilemap.TILED_JSON);
        game.load.image('tiles', 'tmw_desert_spacing.png');

    }

    var map;
    var layer;

    var marker;
    var currentTile;
    var cursors;

    var loaded_game = false;

    munch = function() {
        $.get("/newgame", function(data){
            loaded_game = data;
            console.log(data)
        }).done(create)
    }


    function create() {

        world_builder();

        map.addTilesetImage('Desert', 'tiles');

        currentTile = map.getTile(17, 16);

        layer = map.createLayer('Ground');

        layer.resizeWorld();

        marker = game.add.graphics();
        marker.lineStyle(2, 0x000000, 1);
        marker.drawRect(0, 0, 32, 32);

        cursors = game.input.keyboard.createCursorKeys();
        console.log(Phaser.Keyboard.ctrlKey)
    }

    function world_builder(data) {

        if (loaded_game == false && !data) {
            map = game.add.tilemap('desert');
        } else {
            game.load.tilemap('desert', data, null, Phaser.Tilemap.TILED_JSON);
            map = game.add.tilemap(data);
        }

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



});
