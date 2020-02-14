
I = imread('im1.png');
I_cropped = imcrop(I,[1,1,620,462]);
I_GSC = rgb2gray(I_cropped);
I_BW = imbinarize(I_GSC);

I_BW = imclose(I_BW,strel('disk',16,4));
I_BW = imfill(I_BW,'holes');

I_edge = edge(I_BW,'Canny');


figure
imshow(I_edge)



[Im.x,Im.y] =size(I_edge);
diagLen = round(sqrt(Im.x^2+Im.y^2));


a = zeros(length(Im.x),1);
b = zeros(length(Im.y),1);

p =zeros(Im.x,Im.y,diagLen);
maxVal = zeros(diagLen,1);


for r = 1:45
    maxScore = 8*r;
    
    for i = 1: Im.x
        for j =1: Im.y            
            if I_edge(i,j) == 1                
                for tht = 1:360                   
                   a = round(i-r*cosd(tht));
                   b = round(j-r*sind(tht));  
                   
                      if (a > 0) && (a < Im.x) && (b > 0) && (b <Im.y)
                        if p(a,b,r) < maxScore
                            p(a,b,r) = p(a,b,r)+1;
                            
                        end
                      end 
                      
                end
            end
        end
    end
p_slice = p(:,:,r);
maxVal(r) = max(p_slice(:));  

maxArray = imregionalmax(p_slice);
maxArray = maxArray & p_slice >= (maxVal(r)*0.5) ;

 

end

[~,locations] = findpeaks(p_slice,2,'MinPeakProminence',4,'Threshold',5);

figure
imshow(I_GSC)
hold on




for x = 1:length(locations)
    p_prime = p(:,:,locations(x));
    [~,ind] = max(p_prime(:));
    [row,col] = ind2sub(size(p_prime),ind);
    plot (col,row,'.','markersize',10)
    plotCircle(col,row,locations(x));
end



function plotCircle(x,y,r)
ang=0:360; 
xp=r*cosd(ang);
yp=r*sind(ang);
plot(x+xp,y+yp);
end

