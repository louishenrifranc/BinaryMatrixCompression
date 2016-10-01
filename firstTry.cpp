#include <stdio.h>
#include <fstream>
#include <cmath>
#include <iostream>
#include <cassert>

using namespace std;
// #include "tbb/tbb.h"
const auto binary_matrix_nb_row = 1'000;
const auto binary_matrix_nb_col = 1'000'000;
const auto binary_file_name = "binaryMatrix";



void generateMatrixBinary() {
	ofstream out(binary_file_name);
	for(int i(0);i<binary_matrix_nb_row;i++) {
		for(int j(0);j<binary_matrix_nb_col;j+=3) {
			int k = rand() % 3;
			out << (k == 0 ? 1 : 0) << "," << (k == 1 ? 1 : 0) << "," << (k == 2 ? 1 : 0) << ",";
		}	
		out << endl;
	}
	out.close();
}


class CompressMatrix {
	CompressMatrix(const long int& nbRow,const long int& nbCol,const int& dispersion) :
		m_dispersion(dispersion),
		m_nbRow(nbCol) {
		
		if(dispersion == 1) {
			nbBitForOneFeature = 1;
		} else {
			nbBitForOneFeature = ceil(log(dispersion) / log(2));
		}


		//assert(nbCol % dispersion == 0);

		//m_nbCol = nbCol / dispersion;
		//m_nbCol = ceil((double)(m_nbCol) / 32);
		//m_nbCol *= nbBitForOneFeature;
		m_nbCol = nbCol / 32;

		m_nbRow = nbRow;

		m = (int32_t **) malloc(m_nbRow * sizeof(int32_t*));
	}


	void compressRow(const int& row,const int8_t data[]) {
		assert(row < m_nbRow);
		delete[] m[row];
		m[row] = (int32_t *) malloc(m_nbCol * sizeof(int32_t*));

		unsigned int nbColData = sizeof(data) / sizeof(int8_t);
		for(unsigned int32_t i(0);i<nbColData;i++) {
			int index = m_nbCol / 32;
			int shift = m_nbCol - shift * 32;
			m[row][index] = (data[i] ? (1 << shift) : (0 << shift));
		}
	}

	int8_t nbBitForOneFeature;
	int8_t m_dispersion;
	int32_t ** m;
	int32_t m_nbRow;
	int32_t m_nbCol;
};

void compressMatrixBinary() {
	//ifstream()
}

int main()
{	
	int i[] = {1,2,3,4,5,6,9}	;
	// generateMatrixBinary();
}