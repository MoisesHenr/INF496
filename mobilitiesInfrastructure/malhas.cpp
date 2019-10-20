#include <iostream>
#include <stdlib.h>     /* srand, rand */
#include <time.h>
#include <algorithm>
#include <fstream>

using namespace std;

struct Corner{
    float u; //up
    float d; //down
    float l; //left
    float r; //right
};

Corner block[5][7];
ofstream out;

//arrumar...
void Way (int posI, int posJ, int posIb, int posJb, int &depth) {
    depth++;

    if (depth >= 50) {
        return;
    }

    int u, d, l, r, m;

    u = (rand() % 10 + 1)*block[posI][posJ].u;
    d = (rand() % 10 + 1)*block[posI][posJ].d;
    l = (rand() % 10 + 1)*block[posI][posJ].l;
    r = (rand() % 10 + 1)*block[posI][posJ].r;

    m = max(u, max(d, max(l, r)));

    if (m == u && posI > 0 && posI-1 != posIb) {
        out << "    <moveto x=\"" << posJ*100+20 << "\" y=\"" << (posI-1)*100+10 << "\"/>" << endl;
        Way(posI-1, posJ, posI, posJ, depth);
    }
    else if (m == d && posI < 4 && posI+1 != posIb) {
        out << "    <moveto x=\"" << posJ*100+20 << "\" y=\"" << (posI+1)*100+10 << "\"/>" << endl;
        Way(posI+1, posJ, posI, posJ, depth);
    }
    else if (m == l && posJ > 0 && posJ-1 != posJb) {
        out << "    <moveto x=\"" << (posJ-1)*100+20 << "\" y=\"" << posI*100+10 << "\"/>" << endl;
        Way(posI, posJ-1, posI, posJ, depth);
    }
    else if (m == r && posJ < 6 && posJ+1 != posJb) {
        out << "    <moveto x=\"" << (posJ+1)*100+20 << "\" y=\"" << posI*100+10 << "\"/>" << endl;
        Way(posI, posJ+1, posI, posJ, depth);
    }
    else {
        Way(posI, posJ, posIb, posJb, depth);
    }
}

int main() {
    int posI, posJ, depth = -1;
    int numRoutes;

    cout << "Entre com o numero de rotas desejadas: ";
    cin >> numRoutes;

    for (int j = 0; j < 7; j++) { //line 0 and 2 --- left
        block[0][j].l = 1;
        block[1][j].l = 0;
        block[2][j].l = 2;
        block[3][j].l = 0;
        block[4][j].l = 1;
    }

    for (int j = 0; j < 7; j++) { //line 1, 2 and 3 --- right
        block[0][j].r = 0;
        block[1][j].r = 1;
        block[2][j].r = 2;
        block[3][j].r = 1;
        block[4][j].r = 0;
    }

    for (int i = 0; i < 5; i++) { //row 0, 2 and 4 --- down
        block[i][0].d = 1;
        block[i][1].d = 0;
        block[i][2].d = 2;
        block[i][3].d = 0;
        block[i][4].d = 1;
        block[i][5].d = 0;
        block[i][6].d = 1;
    }

    for (int i = 0; i < 5; i++) { //row 1, 2, 3 and 5 --- up
        block[i][0].u = 0;
        block[i][1].u = 1;
        block[i][2].u = 2;
        block[i][3].u = 1;
        block[i][4].u = 0;
        block[i][5].u = 1;
        block[i][6].u = 0;
    }

    srand (time(NULL));
    for (int iter = 0; iter < numRoutes; iter++) {
        posI = rand() % 5;
        posJ = rand() % 7;

        while (posJ == 0 and posI == 4) {
            //cout << "Posição invalida em: " << iter << endl;
            posI = rand() % 5;
            posJ = rand() % 7;
        }

        string name;
        name = "routes/" + to_string(iter) + ".xml";

        out.open(name);
        out << "<movement>" << endl;
        out << "    <set speed=\"10\" x=\"" << posJ*100+20 << "\" y=\"" << posI*100+10 << "\"/>" << endl;
        Way(posI, posJ, posI, posJ, depth);
        depth = 0;
        out << "</movement>";
        out.close();
    }
    
    cout << "Geração de rotas terminada" << endl;

    return 0;
}
