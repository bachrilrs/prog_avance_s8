public class point{
    double x, y;

    public point(){
        x = 0;
        y = 0;
    }

    public point (double x ,double y){
        this.x = x;
        this.y = y;
    }

    public void deplacer(double dx, double dy){
        x+=dx;
        y+=dy;
    }
}