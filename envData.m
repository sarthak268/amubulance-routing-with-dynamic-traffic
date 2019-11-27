clear all;
close all;

% Environment
numNodes = 100;
Length = 1000;
width = 1200;
maxSpeed = 20; % m/s
minSpeed = 1; % m/s
numHospitals = 5;

% create nodes
xHospitalLocation = Length*rand(numHospitals,1);
yHospitalLocation = width*rand(numHospitals,1);
xNodes = Length*rand(numNodes,1);
yNodes = width*rand(numNodes,1);

Nodes = [xNodes yNodes];
Hospital_Location = [xHospitalLocation yHospitalLocation];

% create delaunay triangulation for roads
dt = delaunayTriangulation(xNodes,yNodes);
dt1 = [dt.ConnectivityList dt.ConnectivityList(:,1)];
dt2 = [dt1(:,1) dt1(:,2); dt1(:,2) dt1(:,3); dt1(:,3) dt1(:,4)];
numEdges = length(dt2);

% create adjacency matrix for edges
adjM = zeros(numNodes+numHospitals,numNodes+numHospitals);
for i = 1:numNodes
    v = find(dt2(:,1) == i);
    adjM(i,dt2(v)) = 1;
    adjM(dt2(v),i) = 1;
end

% connect hospital to the nearest node
% Hospital nodes are from numNodes+1 to numNodes+numHospitals
for i = 1:numHospitals
    dists = sqrt((xHospitalLocation(i)-xNodes(:)).^2 + (yHospitalLocation(i)-yNodes(:)).^2);
    [V,I] = sort(dists);
    adjM(numNodes+i,I(2)) = 1;
    adjM(I(2),numNodes+i) = 1;
end

% create traffic;
edgeSpeeds = ceil(rand(numEdges,1)*maxSpeed);
numHours = 2;
numSeconds = numHours*3600; % hours*seconds
numChanges = numHours/0.25;
trafficChangeTime = ceil(sort(numSeconds*rand(numChanges,1)));
trafficChangeTime = [trafficChangeTime; numSeconds+1]; 
percentageEdgesChangeTraffic = .50;
numEdgeChanges = ceil(numEdges*percentageEdgesChangeTraffic);
maxSpeedChange = 0.25;

% determine the changes whos traffic is changing
% for i = 1:numChanges
%     tempEdgeChanges = ceil(rand(ceil(length(dt2)*percentageEdgesChangeTraffic),1)*length(dt2));
%     trafficChange(i).edges = dt2(edgeChanges,:);
%     trafficChange(i).edgeSpeeds = randn(length(edgeChanges),1)*0.25;
% end

% Accident data
numAccidents = 1000;
accidentKeyNodes = 10;
accidentKeyNodeIndex = ceil(rand(accidentKeyNodes,1)*numNodes);
accidentTimes = sort(ceil(rand(numAccidents,1)*numSeconds));
numNearestNeighbor = 10;
accidentNodes = zeros(numAccidents,1);

for i = 1:numAccidents
    anode = accidentKeyNodeIndex(ceil(rand*accidentKeyNodes));
    dists = sqrt((xNodes(anode)- xNodes(:)).^2 + (yNodes(anode)-yNodes(:)).^2);
    [V,I] = sort(dists);
    accidentNodes(i) = I(ceil(rand*numNearestNeighbor));
end

% accident time and nodes where the accident happens
accidentData = [accidentTimes accidentNodes];    

% time lapse data
trafficData = zeros(numSeconds,numEdges);
trafficChangeFlag = 1;
tempEdgeSpeeds = edgeSpeeds;
for i = 1:numSeconds
    trafficData(i,:) = tempEdgeSpeeds;   
    if i > trafficChangeTime(trafficChangeFlag)
        tempEdgeChanges = ceil(rand(numEdgeChanges,1)*length(dt2));
        for j = 1:length(tempEdgeChanges)
            tempEdgeSpeeds(tempEdgeChanges(j)) = edgeSpeeds(tempEdgeChanges(j)) + newSpeed(edgeSpeeds(tempEdgeChanges(j)),maxSpeedChange);
            trafficData(i,tempEdgeChanges(j)) = tempEdgeSpeeds(tempEdgeChanges(j));
            tempEdgeSpeeds(tempEdgeChanges(j)) = trafficData(i,tempEdgeChanges(j));
        end
        trafficChangeFlag = trafficChangeFlag + 1;        
    end
end


csvwrite('trafficData.csv',trafficData);
csvwrite('collisionData.csv', accidentData);
csvwrite('adjM.csv', adjM);
csvwrite('nodes.csv', Nodes);
csvwrite('hospital.csv', Hospital_Location);
