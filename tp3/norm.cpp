#include <iostream>
#include <vector>
#include <tgmath.h>

using namespace std;

extern "C" {
	float norm(const float* array, int len){
		int n = 2*len;
		float rest = 0.0;
		for(int i=2; i < n; i+= 2){
			rest += sqrt(pow(array[i-2] - array[i],2) + pow(array[i-1]-array[i+1],2));	
		}
		rest += sqrt(pow(array[n-2] - array[0],2) + pow(array[n-1]-array[1],2));	
		
		return rest;
	}

	bool acceptation(float e_old, float e_new, float T, float rand){
		float delta = e_new - e_old;
		srand(time(NULL));

		float P = min((float) 1, exp(-delta / T));

		if (rand < P){
			return true;
		}
		else{
			return false;
		}
	}
}
