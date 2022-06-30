\ Model facility_location
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  - 367 Select[0] - 316 Select[1] - 234 Select[2] - 419 Select[3]
   - 286 Select[4] - 366 Select[5] - 362 Select[6]
   + 4509.988913511872 Assign[0,0] + 10040.91629284897 Assign[0,1]
   + 3705.401462729781 Assign[0,2] + 6276.941930590086 Assign[0,3]
   + 6306.346010171025 Assign[0,4] + 9269.843580125827 Assign[0,5]
   + 5154.609587543949 Assign[0,6] + 2885.441020371191 Assign[1,0]
   + 4513.205669071391 Assign[1,1] + 3765.306044943742 Assign[1,2]
   + 861.2325267042627 Assign[1,3] + 4319.564576337837 Assign[1,4]
   + 4105.875150354758 Assign[1,5] + 4465.302857109943 Assign[1,6]
   + 2004.498439450079 Assign[2,0] + 6728.812023536856 Assign[2,1]
   + 2865.564212655271 Assign[2,2] + 3010.321791298265 Assign[2,3]
   + 6326.555320336758 Assign[2,4] + 6405.124237432849 Assign[2,5]
   + 2563.249694973139 Assign[2,6] + 3844.874542459709 Assign[3,0]
   + 6283.127387243033 Assign[3,1] + 3851.376280978771 Assign[3,2]
   + 3304.514803843836 Assign[3,3] + 2438.159132377184 Assign[3,4]
   + 5470.174773134658 Assign[3,5] + 5646.580423808985 Assign[3,6]
   + 4345.658669218482 Assign[4,0] + 3205.562118716424 Assign[4,1]
   + 5004 Assign[4,2] + 1435.782106327635 Assign[4,3]
   + 2420.609194718914 Assign[4,4] + 2509.992817228333 Assign[4,5]
   + 6207.224967708329 Assign[4,6] + 2510.992817228333 Assign[5,0]
   + 4813.326112068523 Assign[5,1] + 3365.059523282288 Assign[5,2]
   + 766.5773105863909 Assign[5,3] + 4182.319714841085 Assign[5,4]
   + 4346.658669218482 Assign[5,5] + 4182.319714841085 Assign[5,6]
   + 6321.853069855251 Assign[6,0] + 12537.95914452325 Assign[6,1]
   + 5391.164807134504 Assign[6,2] + 8611.230967266363 Assign[6,3]
   + 8864.893836140041 Assign[6,4] + 11785.64345810178 Assign[6,5]
   + 6234.964600958974 Assign[6,6]
Subject To
 Demand[0]: Assign[0,0] + Assign[0,1] + Assign[0,2] + Assign[0,3]
   + Assign[0,4] + Assign[0,5] + Assign[0,6] = 1
 Demand[1]: Assign[1,0] + Assign[1,1] + Assign[1,2] + Assign[1,3]
   + Assign[1,4] + Assign[1,5] + Assign[1,6] = 1
 Demand[2]: Assign[2,0] + Assign[2,1] + Assign[2,2] + Assign[2,3]
   + Assign[2,4] + Assign[2,5] + Assign[2,6] = 1
 Demand[3]: Assign[3,0] + Assign[3,1] + Assign[3,2] + Assign[3,3]
   + Assign[3,4] + Assign[3,5] + Assign[3,6] = 1
 Demand[4]: Assign[4,0] + Assign[4,1] + Assign[4,2] + Assign[4,3]
   + Assign[4,4] + Assign[4,5] + Assign[4,6] = 1
 Demand[5]: Assign[5,0] + Assign[5,1] + Assign[5,2] + Assign[5,3]
   + Assign[5,4] + Assign[5,5] + Assign[5,6] = 1
 Demand[6]: Assign[6,0] + Assign[6,1] + Assign[6,2] + Assign[6,3]
   + Assign[6,4] + Assign[6,5] + Assign[6,6] = 1
Bounds
Binaries
 Select[0] Select[1] Select[2] Select[3] Select[4] Select[5] Select[6]
 Assign[0,0] Assign[0,1] Assign[0,2] Assign[0,3] Assign[0,4] Assign[0,5]
 Assign[0,6] Assign[1,0] Assign[1,1] Assign[1,2] Assign[1,3] Assign[1,4]
 Assign[1,5] Assign[1,6] Assign[2,0] Assign[2,1] Assign[2,2] Assign[2,3]
 Assign[2,4] Assign[2,5] Assign[2,6] Assign[3,0] Assign[3,1] Assign[3,2]
 Assign[3,3] Assign[3,4] Assign[3,5] Assign[3,6] Assign[4,0] Assign[4,1]
 Assign[4,2] Assign[4,3] Assign[4,4] Assign[4,5] Assign[4,6] Assign[5,0]
 Assign[5,1] Assign[5,2] Assign[5,3] Assign[5,4] Assign[5,5] Assign[5,6]
 Assign[6,0] Assign[6,1] Assign[6,2] Assign[6,3] Assign[6,4] Assign[6,5]
 Assign[6,6]
End
