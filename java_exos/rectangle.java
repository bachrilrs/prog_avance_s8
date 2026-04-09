public class rectangle {
    private double centre, longueur, hauteur;

    public rectangle() {
        x = 0; y = 0; longueur = 10; hauteur = 20;
    }
    
    public rectangle(double x, double y, double l, double h) {
        centre = new point(x,y);
        this.longueur = l;
        this.hauteur = h;
    }
    
    public double surface() {
        return longueur * hauteur;
    }
    
    public double perimetre()
    { 
        return 2*(longueur + hauteur);
    }

    public void deplacer(double dx, double dy){
        centre.deplacer(dx,dy);
    }

    public void afficher_info() {
        System.out.println("Le rectangle est en (" + x + "," + y + "), L=" + longueur + ", H=" + hauteur);
    }
}
