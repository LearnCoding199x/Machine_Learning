#include<iostream>
#include<time.h>
#include<math.h>
#include <cstdlib>
using namespace std;

clock_t begin_time;
const int nMax = 100000 + 5 ;
int queen[nMax]; //save the position of nqueen
int cheoxuoi[2*nMax]; // number of parallel line with the secondary diagonal 
int cheonguoc[2*nMax]; // number of parallel line with the principal diagonal
int n=1000; //number  of queens
int step=0; //step

//getPosition of the line parallel with the principal diagonal
int getViTriCheoXuoi(int i){return i+queen[i]-1;
}

//getPosition of the line parallel with the secondary diagonal 
int getViTriCheoNguoc(int i){return i-queen[i]+n;
}	

//init function
void init(){
	for(int i=1;i<=n;i++){
		cheoxuoi[getViTriCheoXuoi(i)]=0;
		cheonguoc[getViTriCheoNguoc(i)]=0;
	}
	for(int i=1;i<=n;i++){
		queen[i]=i;
		cheoxuoi[getViTriCheoXuoi(i)]++;
		cheonguoc[getViTriCheoNguoc(i)]++;
	}
}

//swap 2 queens
void doicho(int u,int v){
	int temp = getViTriCheoXuoi(u);
	cheoxuoi[temp]--;
	temp = getViTriCheoNguoc(u);
	cheonguoc[temp]--;
	temp = getViTriCheoXuoi(v);
	cheoxuoi[temp]--;
	temp=getViTriCheoNguoc(v);
	cheonguoc[temp]--;
	
	swap(queen[u],queen[v]);
	temp = getViTriCheoXuoi(u);
	cheoxuoi[temp]++;
	temp = getViTriCheoNguoc(u);
	cheonguoc[temp]++;
	temp = getViTriCheoXuoi(v);
	cheoxuoi[temp]++;
	temp=getViTriCheoNguoc(v);
	cheonguoc[temp]++;
}

//calculate the danger
int calculate_Heuristic(int u,int v){
	int sum = 0,sum2=0;
	int temp;
	temp = getViTriCheoXuoi(u);
	sum+=cheoxuoi[temp]-1;
	temp = getViTriCheoNguoc(u);
	sum+=cheonguoc[temp]-1;
	temp = getViTriCheoXuoi(v);
	sum+=cheoxuoi[temp]-1;
	temp=getViTriCheoNguoc(v);
	sum+=cheonguoc[temp]-1;
	if(getViTriCheoNguoc(u)==getViTriCheoNguoc(v))	sum--;
	if(getViTriCheoXuoi(u)==getViTriCheoXuoi(v))	sum--;

	doicho(u,v);

	temp = getViTriCheoXuoi(u);
	sum2+=cheoxuoi[temp]-1;
	temp = getViTriCheoNguoc(u);
	sum2+=cheonguoc[temp]-1;
	temp = getViTriCheoXuoi(v);
	sum2+=cheoxuoi[temp]-1;
	temp=getViTriCheoNguoc(v);
	sum2+=cheonguoc[temp]-1;
	if(getViTriCheoNguoc(u)==getViTriCheoNguoc(v))	sum--;
	if(getViTriCheoXuoi(u)==getViTriCheoXuoi(v))	sum--;

	doicho(u,v);

	return sum-sum2;
}


void show(){
	for(int i=1;i<=n;i++)	cout<<i<<" "<<queen[i]<<endl;
}

//Simulated_Annealing
void toithep(){
	double nhietdo=40;
	double haophi=0.01;
	int check = 0;
	while(nhietdo>0.0000001){
		int u,v;
		int tmp[nMax];
		int pos=0;
		for(int i=1;i<=n;i++){
			if(cheoxuoi[getViTriCheoXuoi(i)] > 1 || cheonguoc[getViTriCheoNguoc(i)] > 1){
				pos++;
				tmp[pos] = i;
			}
		}
		if(pos>0){
			step++;
			u = tmp[1+rand()%pos];
			v = rand()%(n-1)+1;
			if(u==v)	v++;
			int t = calculate_Heuristic(u,v);
			if(t>0){
				doicho(u,v);
				nhietdo-=haophi*nhietdo;
			}
			else{
				double random = (double)(rand()%1000) / 1000.0;
				double kq = (double)exp(t-1/nhietdo);
				if(random<=kq){
					doicho(u,v);
					nhietdo-=haophi*nhietdo;
				}
			}
		}
		else{
			check = 1;
			break;
		}
	}
	if(check){
		cout<<step<<endl;
		show();
	}
}

main(){
	clock_t bgcl = clock();
	cout<<"Nhap so n : "<<endl;
	cin>>n;
	begin_time = clock();
	init();
	toithep();
	cout << endl << "Total time    : " << (float) (clock() - bgcl )/  CLOCKS_PER_SEC<<"s"<<endl;
}


