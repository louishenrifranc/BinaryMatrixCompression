#include <stdio.h>
#include <fstream>
#include <cmath>
#include <iostream>
#include <cassert>
#include <ctime>
#include <chrono>

using namespace std;
// #include "tbb/tbb.h"
const auto binary_matrix_nb_row = 1'000;
const auto binary_matrix_nb_col = 1'000'000;
const auto binary_file_name = "binaryMatrix";



void generateMatrixBinary() {
        ofstream out(binary_file_name);
        for (int i(0); i < binary_matrix_nb_row; i++) {
                for (int j(0); j < binary_matrix_nb_col; j += 3) {
                        int k = rand() % 3;
                        out << (k == 0 ? 1 : 0) << "," << (k == 1 ? 1 : 0) << "," << (k == 2 ? 1 : 0) << ",";
                }
                out << endl;
        }
        out.close();
}


class CompressMatrix {
public:
        CompressMatrix(const long int& nbRow, const long int& nbCol, const int& dispersion) :
                m_nbRow(nbRow),
                m_oldnbCol(nbCol),
                m_nbCol(ceil((double)(nbCol) / 32))
        {
                m = ((uint32_t **)malloc(m_nbRow * sizeof(uint32_t *)));
        }


        ~CompressMatrix() {
                for (int32_t row(0); row < m_nbRow; row++) {
                        // delete[] m[row];
                }
        }
        void compressRow(const int& row, const int8_t* data, const int& N) {
                assert(row < m_nbRow);
                // delete[] m[row];
                m[row] = (uint32_t  *)malloc(m_nbCol * sizeof(uint32_t *));
                memset(m[row], 0, m_nbCol * sizeof(m[row]));
                for (uint32_t i(0); i < N; i++) {
                        int index = i / 32;
                        int shift = i - index * 32;
                        m[row][index] += (data[i] ? (1 << shift) : (0 << shift));
                }
        }

        void decompressRow(const int& row, int8_t* data) {
                memset(data, 0, (m_oldnbCol) * sizeof(int8_t));
                for (int i(0); i < m_oldnbCol; i++) {
                        int index = i / 32;
                        int8_t shift = i - index * 32;
                        data[i] = ((m[row][index] & (1 << shift)) ? 1 : 0);
                }
        }

        inline float multiplyRow(const int& row, const float* rowA) {
                float result = 0;
                auto m_row = m[row];
                for (int i(0); i < m_oldnbCol; i++) {
                        int index = i / 32;
                        int8_t shift = i - index * 32;
                        int bit = m[row][index] & (1 << shift);
                        float value = rowA[i];
                        result += ((m[row][index] & (1 << shift)) ? rowA[i] : 0);
                }
                return result;
        }

        uint32_t **m;
        uint32_t  m_nbRow;
        uint32_t  m_oldnbCol;
        uint32_t  m_nbCol;
};

void testCompression() {
        CompressMatrix cp(100, 1000, 1);
        int8_t data[1000];
        for (int i(0); i < 1000; i++) {
                data[i] = rand() % 2;
        }


        size_t N = sizeof(data) / sizeof(data[0]);

        auto start = chrono::high_resolution_clock::now();
        cp.compressRow(1, data, N);
        auto end = chrono::high_resolution_clock::now();
        chrono::duration<double> diff = end - start;
        cout << "Compressing row of size " << N << " :" << diff.count() << " s\n";

        int8_t data_uncompress[1001];
        start = chrono::high_resolution_clock::now();
        cp.decompressRow(1, data_uncompress);
        end = chrono::high_resolution_clock::now();
        diff = end - start;
        cout << "Decompressing row of size " << N << " :" << diff.count() << " s\n";
        for (int i(0); i < 1000; i++) {
                assert((data[i]) == (data_uncompress[i]));
        }
}



void testMultiplyMatrix() {
        const int sizeColomn = 1'000'000;
        CompressMatrix cp(100, sizeColomn, 1);
        int8_t data[sizeColomn];
        for (int i(0); i < sizeColomn; i++) {
                data[i] = rand() % 2;
        }

        size_t N = sizeof(data) / sizeof(data[0]);
        cp.compressRow(1, data, N);


        float* array;
        array = (float *)malloc(sizeColomn * sizeof(float));

        for (int i(0); i < sizeColomn; i++) {
                array[i] = (float)rand() / (float)(RAND_MAX / 5.0);
        }


        float result = 0, result1 = 0;
        auto start = chrono::high_resolution_clock::now();
        for (int i(0); i < sizeColomn; i++) {
                result += data[i] * array[i];
        }
        auto end = chrono::high_resolution_clock::now();
        chrono::duration<double> diff = end - start;
        cout << "Simple multiplication  :" << diff.count() << " s\n";


        start = chrono::high_resolution_clock::now();
        result1 = cp.multiplyRow(1, array);
        end = chrono::high_resolution_clock::now();
        diff = end - start;




        cout << "Fancy row multiplication  :" << diff.count() << " s\n";

        assert(result == result1);
}

int main()
{
        srand(time(nullptr));
        int i[] = { 1,2,3,4,5,6,9 };
        // generateMatrixBinary();
        testCompression();
        testMultiplyMatrix();
}

