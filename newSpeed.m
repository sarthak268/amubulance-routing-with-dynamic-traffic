function speedChange = newSpeed(orgSpeed, percentageChange)

sign = rand;
if sign < 0.5
    sign = -1;
else
    sign = 1;
end

speedChange = sign*orgSpeed*percentageChange;
end