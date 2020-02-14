
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
centers = zeros(Im.x,Im.y);


for r = 1:100
    maxScore = r^2;
    
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
    
end

[~,locations] = findpeaks(maxVal,'MinPeakProminence',4,'Threshold',5);


for x = 1:numel(locations)
    p_prime = p(:,:,locations(x));
    a= max(p_prime(:));
    centers = centers + (p_prime > (0.8*a));
end

% If you Imshow(ab) you can see the centers, the issues is there are 15 pts
% (some are grouped) and I need to eliminate the false centers without
% removing the actual centers



%figure
%imshow(I_GSC)
%hold on

function plotCircle(x,y,r)
ang=0:360; 
xp=r*cosd(ang);
yp=r*sind(ang);
plot(x+xp,y+yp);
end

