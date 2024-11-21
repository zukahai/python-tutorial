game_W = 800, game_H = 600;

mapImage = new Image();
mapImage.src = "map1.png";


class game {
    constructor() {
        this.canvas = document.createElement("canvas");
        this.context = this.canvas.getContext("2d");
        this.canvas.width = game_W;
        this.canvas.height = game_H;
        document.body.appendChild(this.canvas);

        this.listenMouse();
        this.listenTouch();
        this.listenKey();

        this.listPoint = [];
        this.startFPS(30);
    }

    // hàm chạy game theo fps của máy
    start(timestamp) {
        this.update();
        requestAnimationFrame((timestamp) => this.start(timestamp));
    }

    // hàm chạy game theo fps cố định
    startFPS(fps) {
        this.update();
        
        setTimeout(() => {
            this.startFPS(fps);
        }, 1000/fps);
    }

    // hàm cập nhật game
    update() {
        this.clearScreen();
        this.draw();
    }

    // hàm lắng nghe sự kiện chuột
    listenMouse() {
        document.addEventListener("mousedown", evt => {
            var x = evt.offsetX == undefined ? evt.layerX : evt.offsetX;
            var y = evt.offsetY == undefined ? evt.layerY : evt.offsetY;
            console.log("Mouse Down " + x + " " + y);
            this.listPoint.push({x: x, y: y});
        })

        document.addEventListener("mousemove", evt => {
            var x = evt.offsetX == undefined ? evt.layerX : evt.offsetX;
            var y = evt.offsetY == undefined ? evt.layerY : evt.offsetY;
            // console.log("Mouse Move " + x + " " + y);
            

        })

        document.addEventListener("mouseup", evt => {
            var x = evt.offsetX == undefined ? evt.layerX : evt.offsetX;
            var y = evt.offsetY == undefined ? evt.layerY : evt.offsetY;
            console.log("Mouse Up " + x + " " + y);
        })
    }

    // hàm lắng nghe sự kiện touch
    listenTouch() {
        document.addEventListener("touchmove", evt => {
            var y = evt.touches[0].pageY;
            var x = evt.touches[0].pageX;
        })

        document.addEventListener("touchstart", evt => {
            let y = evt.touches[0].pageY;
            let x = evt.touches[0].pageX;

        })

        document.addEventListener("touchend", evt => {
            let x = x_touch;
            let y = y_touch;
        })
    }

    // hàm lắng nghe sự kiện phím
    listenKey() {
        document.addEventListener("keydown", evt => {
            console.log(evt.keyCode);
        })

        document.addEventListener("keyup", evt => {
            console.log(evt.keyCode);
        });
    }

    // hàm vẽ các thành phần
    draw() {
        this.clearScreen();
        // draw map
        this.context.drawImage(mapImage, 0, 0, game_W, game_H);

        // draw point
        this.context.fillStyle = "#FF0000";
        for (let i = 0; i < this.listPoint.length; i++) {
            this.context.fillRect(this.listPoint[i].x, this.listPoint[i].y, 20, 20);
        }
    }


    // hàm xoá những gì đã vẽ
    clearScreen() {
        this.context.clearRect(0, 0, game_W, game_H);
        this.context.fillStyle = "#000000";
        this.context.fillRect(0, 0, game_W, game_H);
    }


    // luôn cho game full màn hình
    render() {
        if (this.canvas.width != document.documentElement.clientWidth || this.canvas.height != document.documentElement.clientHeight) {
            this.canvas.width = document.documentElement.clientWidth;
            this.canvas.height = document.documentElement.clientHeight;
            game_W = this.canvas.width;
            game_H = this.canvas.height;
        }
    }

}

var g = new game();