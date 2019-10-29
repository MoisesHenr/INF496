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

ofstream out;
int valx = 9, valy = 6;
Corner block[7][10];

void Way (int posY, int posX, int posYb, int posXb, int &depth) {
	depth++;

	if (depth >= 50) {
		return;
	}

	int u, d, l, r, m;

	u = (rand() % 10 + 1)*block[posY][posX].u;
	d = (rand() % 10 + 1)*block[posY][posX].d;
	l = (rand() % 10 + 1)*block[posY][posX].l;
	r = (rand() % 10 + 1)*block[posY][posX].r;

	m = max(u, max(d, max(l, r)));

	if (m == u && posY > 0 && posY-1 != posYb) {
		out << "    <moveto x=\"" << posX*100 << "\" y=\"" << (posY-1)*100 << "\"/>" << endl;
		Way(posY-1, posX, posY, posX, depth);
	}
	else if (m == d && posY < valy && posY+1 != posYb) {
		out << "    <moveto x=\"" << posX*100 << "\" y=\"" << (posY+1)*100 << "\"/>" << endl;
		Way(posY+1, posX, posY, posX, depth);
	}
	else if (m == l && posX > 0 && posX-1 != posXb) {
		out << "    <moveto x=\"" << (posX-1)*100 << "\" y=\"" << posY*100 << "\"/>" << endl;
		Way(posY, posX-1, posY, posX, depth);
	}
	else if (m == r && posX < valx && posX+1 != posXb) {
		out << "    <moveto x=\"" << (posX+1)*100 << "\" y=\"" << posY*100 << "\"/>" << endl;
		Way(posY, posX+1, posY, posX, depth);
	}
	else {
		Way(posY, posX, posYb, posXb, depth);
	}
}

int main() {
	int posY, posX, depth = -1;
	int numRoutes;

	cout << "Entre com o numero de rotas desejadas: ";
	cin >> numRoutes;
	
	for (int i = 0; i < valy + 1; i++) {
		for (int j = 0; j < valx + 1; j++) {
			if (j % 2 == 0) {
				block[i][j].u = 0;
				block[i][j].d = 1;
			}
			else {
				block[i][j].u = 1;
				block[i][j].d = 0;
			}
			if (i % 2 == 0) {
				block[i][j].l = 0;
				block[i][j].r = 1;
			}
			else {
				block[i][j].l = 1;
				block[i][j].r = 0;
			}
		}
	}

	/*cout << "Trajeto UP: " << endl;
	for (int i = 0; i < valy + 1; i++) {
		for (int j = 0; j < valx + 1; j++) {
			cout << block[i][j].u << " ";
		}
		cout << endl;
	}
	cout << endl;
	cout << "Trajeto DOWN: " << endl;
	for (int i = 0; i < valy + 1; i++) {
		for (int j = 0; j < valx + 1; j++) {
			cout << block[i][j].d << " ";
		}
		cout << endl;
	}
	cout << endl;
	cout << "Trajeto LEFT: " << endl;
	for (int i = 0; i < valy + 1; i++) {
		for (int j = 0; j < valx + 1; j++) {
			cout << block[i][j].l << " ";
		}
		cout << endl;
	}
	cout << endl;
	cout << "Trajeto RIGHT: " << endl;
	for (int i = 0; i < valy + 1; i++) {
		for (int j = 0; j < valx + 1; j++) {
			cout << block[i][j].r << " ";
		}
		cout << endl;
	}
	cout << endl;*/

	srand (time(NULL));
	for (int iter = 0; iter < numRoutes; iter++) {
		posY = rand() % (valy + 1);
		posX = rand() % (valx + 1);

		while (posX == 0 && posY == valy) {
			posY = rand() % (valy + 1);
			posX = rand() % (valx + 1);
		}

		string name;
		name = "routes/" + to_string(iter) + ".xml";

		out.open(name);
		out << "<movement>" << endl;
		out << "    <set speed=\"10\" x=\"" << posX*100 << "\" y=\"" << posY*100 << "\"/>" << endl;
		Way(posY, posX, posY, posX, depth);
		depth = 0;
		out << "</movement>";
		out.close();
	}
	
	cout << "Geração de rotas terminada" << endl;

	return 0;
}
