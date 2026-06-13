#include<stdio.h>

float absVal(float x){
    if(x<0) return (-x);
    else return x;
}

typedef struct {
    float x;
    float y;
} Point;


typedef struct {
    Point top_left;
    Point bottom_right;
} Rectangle;

Rectangle init(float x1, float x2, float y1, float y2){
    Rectangle r;
    r.top_left.x=x1;
    r.top_left.y=y1;
    r.bottom_right.x=x2;
    r.bottom_right.y=y2;
    return r;
}

float getBase(Rectangle r){
    float base=absVal(r.top_left.x-r.bottom_right.x);
    return base;
}

float getHeight(Rectangle r){
    float height=absVal(r.top_left.y-r.bottom_right.y);
    return height;
}

float getArea(Rectangle r){
    float area=getBase(r)*getHeight(r);
    return area;
}

int main(){

    Rectangle rett= init(4.0,6.0,8.0,2.0);
    printf("%f \n %f \n %f \n",getBase(rett),getHeight(rett),getArea(rett));


    return 0;
}