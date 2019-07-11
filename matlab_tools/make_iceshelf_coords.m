%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Stolen from Ole Richter at:
% https://github.com/kuechenrole/antarctic_melting/blob/master/matlab_scripts/make_iceshelf_coords.m
%
% adapted by Eva Cougnon 
% created: June 2019
% last modif: July 2019
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Chad Green toolbox
addpath AntarcticMappingTools/
addpath antbounds/

% from the antbounds toolbox (Chad Green)
load antbounds/iceshelves_2008_v2.mat

[xgrid,ygrid] = psgrid(-90,0,5510,5,'xy');
%plot(xgrid,ygrid,'.','color',0.8*[1 1 1])
%hold on
%antbounds('gl','k')
%antbounds('coast','k')
%antbounds('shelves','k')
shelf = isiceshelf(xgrid,ygrid);
%plot(xgrid(shelf),ygrid(shelf),'kx')


for i=1:length(name)
shelf=name{i};
shelves(i).name=shelf;
[wx,wy] = antbounds_data(shelf,'xy');
shelf_poly = inpolygon(xgrid,ygrid,wx,wy);
%plot(xgrid(shelf_poly),ygrid(shelf_poly),'ro')
[shelves(i).lat,shelves(i).lon] = ps2ll(xgrid(shelf_poly),ygrid(shelf_poly));
end

save('shelves.mat','shelves')

