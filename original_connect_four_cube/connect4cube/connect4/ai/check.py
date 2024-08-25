# Generated file
from connect4cube.connect4.ai.board import CBoard


def is_win(board: CBoard, move_id: int) -> bool:
    return checkmap[move_id](board.cube, board.current_player)


def is_win0(b, c):
    return (c == b[1] and c == b[2] and c == b[3]) \
        or (c == b[5] and c == b[10] and c == b[15]) \
        or (c == b[6] and c == b[12] and c == b[18]) \
        or (c == b[26] and c == b[52] and c == b[78]) \
        or (c == b[30] and c == b[60] and c == b[90]) \
        or (c == b[31] and c == b[62] and c == b[93])


def is_win1(b, c):
    return (c == b[2] and c == b[3] and (c == b[0] or c == b[4])) \
        or (c == b[6] and c == b[11] and c == b[16]) \
        or (c == b[31] and c == b[61] and c == b[91])


def is_win2(b, c):
    return (c == b[1] and c == b[3] and (c == b[0] or c == b[4])) \
        or (c == b[7] and c == b[12] and c == b[17]) \
        or (c == b[32] and c == b[62] and c == b[92])


def is_win3(b, c):
    return (c == b[1] and c == b[2] and (c == b[0] or c == b[4])) \
        or (c == b[8] and c == b[13] and c == b[18]) \
        or (c == b[33] and c == b[63] and c == b[93])


def is_win4(b, c):
    return (c == b[1] and c == b[2] and c == b[3]) \
        or (c == b[9] and c == b[14] and c == b[19]) \
        or (c == b[34] and c == b[64] and c == b[94])


def is_win5(b, c):
    return (c == b[6] and c == b[7] and c == b[8]) \
        or (c == b[10] and c == b[15] and (c == b[0] or c == b[20])) \
        or (c == b[31] and c == b[57] and c == b[83])


def is_win6(b, c):
    return (c == b[7] and c == b[8] and (c == b[5] or c == b[9])) \
        or (c == b[11] and c == b[16] and (c == b[1] or c == b[21])) \
        or (c == b[12] and c == b[18] and (c == b[0] or c == b[24]))


def is_win7(b, c):
    return (c == b[6] and c == b[8] and (c == b[5] or c == b[9])) \
        or (c == b[12] and c == b[17] and (c == b[2] or c == b[22]))


def is_win8(b, c):
    return (c == b[6] and c == b[7] and (c == b[5] or c == b[9])) \
        or (c == b[13] and c == b[18] and (c == b[3] or c == b[23]))


def is_win9(b, c):
    return (c == b[6] and c == b[7] and c == b[8]) \
        or (c == b[14] and c == b[19] and (c == b[4] or c == b[24]))


def is_win10(b, c):
    return (c == b[11] and c == b[12] and c == b[13]) \
        or (c == b[5] and c == b[15] and (c == b[0] or c == b[20])) \
        or (c == b[36] and c == b[62] and c == b[88])


def is_win11(b, c):
    return (c == b[12] and c == b[13] and (c == b[10] or c == b[14])) \
        or (c == b[6] and c == b[16] and (c == b[1] or c == b[21]))


def is_win12(b, c):
    return (c == b[11] and c == b[13] and (c == b[10] or c == b[14])) \
        or (c == b[7] and c == b[17] and (c == b[2] or c == b[22])) \
        or (c == b[6] and c == b[18] and (c == b[0] or c == b[24]))


def is_win13(b, c):
    return (c == b[11] and c == b[12] and (c == b[10] or c == b[14])) \
        or (c == b[8] and c == b[18] and (c == b[3] or c == b[23]))


def is_win14(b, c):
    return (c == b[11] and c == b[12] and c == b[13]) \
        or (c == b[9] and c == b[19] and (c == b[4] or c == b[24]))


def is_win15(b, c):
    return (c == b[16] and c == b[17] and c == b[18]) \
        or (c == b[5] and c == b[10] and (c == b[0] or c == b[20])) \
        or (c == b[41] and c == b[67] and c == b[93])


def is_win16(b, c):
    return (c == b[17] and c == b[18] and (c == b[15] or c == b[19])) \
        or (c == b[6] and c == b[11] and (c == b[1] or c == b[21]))


def is_win17(b, c):
    return (c == b[16] and c == b[18] and (c == b[15] or c == b[19])) \
        or (c == b[7] and c == b[12] and (c == b[2] or c == b[22]))


def is_win18(b, c):
    return (c == b[16] and c == b[17] and (c == b[15] or c == b[19])) \
        or (c == b[8] and c == b[13] and (c == b[3] or c == b[23])) \
        or (c == b[6] and c == b[12] and (c == b[0] or c == b[24]))


def is_win19(b, c):
    return (c == b[16] and c == b[17] and c == b[18]) \
        or (c == b[9] and c == b[14] and (c == b[4] or c == b[24]))


def is_win20(b, c):
    return (c == b[21] and c == b[22] and c == b[23]) \
        or (c == b[5] and c == b[10] and c == b[15]) \
        or (c == b[46] and c == b[72] and c == b[98])


def is_win21(b, c):
    return (c == b[22] and c == b[23] and (c == b[20] or c == b[24])) \
        or (c == b[6] and c == b[11] and c == b[16])


def is_win22(b, c):
    return (c == b[21] and c == b[23] and (c == b[20] or c == b[24])) \
        or (c == b[7] and c == b[12] and c == b[17])


def is_win23(b, c):
    return (c == b[21] and c == b[22] and (c == b[20] or c == b[24])) \
        or (c == b[8] and c == b[13] and c == b[18])


def is_win24(b, c):
    return (c == b[21] and c == b[22] and c == b[23]) \
        or (c == b[9] and c == b[14] and c == b[19]) \
        or (c == b[6] and c == b[12] and c == b[18])


def is_win25(b, c):
    return (c == b[26] and c == b[27] and c == b[28]) \
        or (c == b[30] and c == b[35] and c == b[40]) \
        or (c == b[31] and c == b[37] and c == b[43])


def is_win26(b, c):
    return (c == b[27] and c == b[28] and (c == b[25] or c == b[29])) \
        or (c == b[31] and c == b[36] and c == b[41]) \
        or (c == b[52] and c == b[78] and (c == b[0] or c == b[104]))


def is_win27(b, c):
    return (c == b[26] and c == b[28] and (c == b[25] or c == b[29])) \
        or (c == b[32] and c == b[37] and c == b[42])


def is_win28(b, c):
    return (c == b[26] and c == b[27] and (c == b[25] or c == b[29])) \
        or (c == b[33] and c == b[38] and c == b[43])


def is_win29(b, c):
    return (c == b[26] and c == b[27] and c == b[28]) \
        or (c == b[34] and c == b[39] and c == b[44])


def is_win30(b, c):
    return (c == b[31] and c == b[32] and c == b[33]) \
        or (c == b[35] and c == b[40] and (c == b[25] or c == b[45])) \
        or (c == b[60] and c == b[90] and (c == b[0] or c == b[120]))


def is_win31(b, c):
    return (c == b[32] and c == b[33] and (c == b[30] or c == b[34])) \
        or (c == b[36] and c == b[41] and (c == b[26] or c == b[46])) \
        or (c == b[37] and c == b[43] and (c == b[25] or c == b[49])) \
        or (c == b[57] and c == b[83] and (c == b[5] or c == b[109])) \
        or (c == b[61] and c == b[91] and (c == b[1] or c == b[121])) \
        or (c == b[62] and c == b[93] and (c == b[0] or c == b[124]))


def is_win32(b, c):
    return (c == b[31] and c == b[33] and (c == b[30] or c == b[34])) \
        or (c == b[37] and c == b[42] and (c == b[27] or c == b[47])) \
        or (c == b[62] and c == b[92] and (c == b[2] or c == b[122]))


def is_win33(b, c):
    return (c == b[31] and c == b[32] and (c == b[30] or c == b[34])) \
        or (c == b[38] and c == b[43] and (c == b[28] or c == b[48])) \
        or (c == b[63] and c == b[93] and (c == b[3] or c == b[123]))


def is_win34(b, c):
    return (c == b[31] and c == b[32] and c == b[33]) \
        or (c == b[39] and c == b[44] and (c == b[29] or c == b[49])) \
        or (c == b[64] and c == b[94] and (c == b[4] or c == b[124]))


def is_win35(b, c):
    return (c == b[36] and c == b[37] and c == b[38]) \
        or (c == b[30] and c == b[40] and (c == b[25] or c == b[45]))


def is_win36(b, c):
    return (c == b[37] and c == b[38] and (c == b[35] or c == b[39])) \
        or (c == b[31] and c == b[41] and (c == b[26] or c == b[46])) \
        or (c == b[62] and c == b[88] and (c == b[10] or c == b[114]))


def is_win37(b, c):
    return (c == b[36] and c == b[38] and (c == b[35] or c == b[39])) \
        or (c == b[32] and c == b[42] and (c == b[27] or c == b[47])) \
        or (c == b[31] and c == b[43] and (c == b[25] or c == b[49]))


def is_win38(b, c):
    return (c == b[36] and c == b[37] and (c == b[35] or c == b[39])) \
        or (c == b[33] and c == b[43] and (c == b[28] or c == b[48]))


def is_win39(b, c):
    return (c == b[36] and c == b[37] and c == b[38]) \
        or (c == b[34] and c == b[44] and (c == b[29] or c == b[49]))


def is_win40(b, c):
    return (c == b[41] and c == b[42] and c == b[43]) \
        or (c == b[30] and c == b[35] and (c == b[25] or c == b[45]))


def is_win41(b, c):
    return (c == b[42] and c == b[43] and (c == b[40] or c == b[44])) \
        or (c == b[31] and c == b[36] and (c == b[26] or c == b[46])) \
        or (c == b[67] and c == b[93] and (c == b[15] or c == b[119]))


def is_win42(b, c):
    return (c == b[41] and c == b[43] and (c == b[40] or c == b[44])) \
        or (c == b[32] and c == b[37] and (c == b[27] or c == b[47]))


def is_win43(b, c):
    return (c == b[41] and c == b[42] and (c == b[40] or c == b[44])) \
        or (c == b[33] and c == b[38] and (c == b[28] or c == b[48])) \
        or (c == b[31] and c == b[37] and (c == b[25] or c == b[49]))


def is_win44(b, c):
    return (c == b[41] and c == b[42] and c == b[43]) \
        or (c == b[34] and c == b[39] and (c == b[29] or c == b[49]))


def is_win45(b, c):
    return (c == b[46] and c == b[47] and c == b[48]) \
        or (c == b[30] and c == b[35] and c == b[40])


def is_win46(b, c):
    return (c == b[47] and c == b[48] and (c == b[45] or c == b[49])) \
        or (c == b[31] and c == b[36] and c == b[41]) \
        or (c == b[72] and c == b[98] and (c == b[20] or c == b[124]))


def is_win47(b, c):
    return (c == b[46] and c == b[48] and (c == b[45] or c == b[49])) \
        or (c == b[32] and c == b[37] and c == b[42])


def is_win48(b, c):
    return (c == b[46] and c == b[47] and (c == b[45] or c == b[49])) \
        or (c == b[33] and c == b[38] and c == b[43])


def is_win49(b, c):
    return (c == b[46] and c == b[47] and c == b[48]) \
        or (c == b[34] and c == b[39] and c == b[44]) \
        or (c == b[31] and c == b[37] and c == b[43])


def is_win50(b, c):
    return (c == b[51] and c == b[52] and c == b[53]) \
        or (c == b[55] and c == b[60] and c == b[65]) \
        or (c == b[56] and c == b[62] and c == b[68])


def is_win51(b, c):
    return (c == b[52] and c == b[53] and (c == b[50] or c == b[54])) \
        or (c == b[56] and c == b[61] and c == b[66])


def is_win52(b, c):
    return (c == b[51] and c == b[53] and (c == b[50] or c == b[54])) \
        or (c == b[57] and c == b[62] and c == b[67]) \
        or (c == b[26] and c == b[78] and (c == b[0] or c == b[104]))


def is_win53(b, c):
    return (c == b[51] and c == b[52] and (c == b[50] or c == b[54])) \
        or (c == b[58] and c == b[63] and c == b[68])


def is_win54(b, c):
    return (c == b[51] and c == b[52] and c == b[53]) \
        or (c == b[59] and c == b[64] and c == b[69])


def is_win55(b, c):
    return (c == b[56] and c == b[57] and c == b[58]) \
        or (c == b[60] and c == b[65] and (c == b[50] or c == b[70]))


def is_win56(b, c):
    return (c == b[57] and c == b[58] and (c == b[55] or c == b[59])) \
        or (c == b[61] and c == b[66] and (c == b[51] or c == b[71])) \
        or (c == b[62] and c == b[68] and (c == b[50] or c == b[74]))


def is_win57(b, c):
    return (c == b[56] and c == b[58] and (c == b[55] or c == b[59])) \
        or (c == b[62] and c == b[67] and (c == b[52] or c == b[72])) \
        or (c == b[31] and c == b[83] and (c == b[5] or c == b[109]))


def is_win58(b, c):
    return (c == b[56] and c == b[57] and (c == b[55] or c == b[59])) \
        or (c == b[63] and c == b[68] and (c == b[53] or c == b[73]))


def is_win59(b, c):
    return (c == b[56] and c == b[57] and c == b[58]) \
        or (c == b[64] and c == b[69] and (c == b[54] or c == b[74]))


def is_win60(b, c):
    return (c == b[61] and c == b[62] and c == b[63]) \
        or (c == b[55] and c == b[65] and (c == b[50] or c == b[70])) \
        or (c == b[30] and c == b[90] and (c == b[0] or c == b[120]))


def is_win61(b, c):
    return (c == b[62] and c == b[63] and (c == b[60] or c == b[64])) \
        or (c == b[56] and c == b[66] and (c == b[51] or c == b[71])) \
        or (c == b[31] and c == b[91] and (c == b[1] or c == b[121]))


def is_win62(b, c):
    return (c == b[61] and c == b[63] and (c == b[60] or c == b[64])) \
        or (c == b[57] and c == b[67] and (c == b[52] or c == b[72])) \
        or (c == b[56] and c == b[68] and (c == b[50] or c == b[74])) \
        or (c == b[36] and c == b[88] and (c == b[10] or c == b[114])) \
        or (c == b[32] and c == b[92] and (c == b[2] or c == b[122])) \
        or (c == b[31] and c == b[93] and (c == b[0] or c == b[124]))


def is_win63(b, c):
    return (c == b[61] and c == b[62] and (c == b[60] or c == b[64])) \
        or (c == b[58] and c == b[68] and (c == b[53] or c == b[73])) \
        or (c == b[33] and c == b[93] and (c == b[3] or c == b[123]))


def is_win64(b, c):
    return (c == b[61] and c == b[62] and c == b[63]) \
        or (c == b[59] and c == b[69] and (c == b[54] or c == b[74])) \
        or (c == b[34] and c == b[94] and (c == b[4] or c == b[124]))


def is_win65(b, c):
    return (c == b[66] and c == b[67] and c == b[68]) \
        or (c == b[55] and c == b[60] and (c == b[50] or c == b[70]))


def is_win66(b, c):
    return (c == b[67] and c == b[68] and (c == b[65] or c == b[69])) \
        or (c == b[56] and c == b[61] and (c == b[51] or c == b[71]))


def is_win67(b, c):
    return (c == b[66] and c == b[68] and (c == b[65] or c == b[69])) \
        or (c == b[57] and c == b[62] and (c == b[52] or c == b[72])) \
        or (c == b[41] and c == b[93] and (c == b[15] or c == b[119]))


def is_win68(b, c):
    return (c == b[66] and c == b[67] and (c == b[65] or c == b[69])) \
        or (c == b[58] and c == b[63] and (c == b[53] or c == b[73])) \
        or (c == b[56] and c == b[62] and (c == b[50] or c == b[74]))


def is_win69(b, c):
    return (c == b[66] and c == b[67] and c == b[68]) \
        or (c == b[59] and c == b[64] and (c == b[54] or c == b[74]))


def is_win70(b, c):
    return (c == b[71] and c == b[72] and c == b[73]) \
        or (c == b[55] and c == b[60] and c == b[65])


def is_win71(b, c):
    return (c == b[72] and c == b[73] and (c == b[70] or c == b[74])) \
        or (c == b[56] and c == b[61] and c == b[66])


def is_win72(b, c):
    return (c == b[71] and c == b[73] and (c == b[70] or c == b[74])) \
        or (c == b[57] and c == b[62] and c == b[67]) \
        or (c == b[46] and c == b[98] and (c == b[20] or c == b[124]))


def is_win73(b, c):
    return (c == b[71] and c == b[72] and (c == b[70] or c == b[74])) \
        or (c == b[58] and c == b[63] and c == b[68])


def is_win74(b, c):
    return (c == b[71] and c == b[72] and c == b[73]) \
        or (c == b[59] and c == b[64] and c == b[69]) \
        or (c == b[56] and c == b[62] and c == b[68])


def is_win75(b, c):
    return (c == b[76] and c == b[77] and c == b[78]) \
        or (c == b[80] and c == b[85] and c == b[90]) \
        or (c == b[81] and c == b[87] and c == b[93])


def is_win76(b, c):
    return (c == b[77] and c == b[78] and (c == b[75] or c == b[79])) \
        or (c == b[81] and c == b[86] and c == b[91])


def is_win77(b, c):
    return (c == b[76] and c == b[78] and (c == b[75] or c == b[79])) \
        or (c == b[82] and c == b[87] and c == b[92])


def is_win78(b, c):
    return (c == b[76] and c == b[77] and (c == b[75] or c == b[79])) \
        or (c == b[83] and c == b[88] and c == b[93]) \
        or (c == b[26] and c == b[52] and (c == b[0] or c == b[104]))


def is_win79(b, c):
    return (c == b[76] and c == b[77] and c == b[78]) \
        or (c == b[84] and c == b[89] and c == b[94])


def is_win80(b, c):
    return (c == b[81] and c == b[82] and c == b[83]) \
        or (c == b[85] and c == b[90] and (c == b[75] or c == b[95]))


def is_win81(b, c):
    return (c == b[82] and c == b[83] and (c == b[80] or c == b[84])) \
        or (c == b[86] and c == b[91] and (c == b[76] or c == b[96])) \
        or (c == b[87] and c == b[93] and (c == b[75] or c == b[99]))


def is_win82(b, c):
    return (c == b[81] and c == b[83] and (c == b[80] or c == b[84])) \
        or (c == b[87] and c == b[92] and (c == b[77] or c == b[97]))


def is_win83(b, c):
    return (c == b[81] and c == b[82] and (c == b[80] or c == b[84])) \
        or (c == b[88] and c == b[93] and (c == b[78] or c == b[98])) \
        or (c == b[31] and c == b[57] and (c == b[5] or c == b[109]))


def is_win84(b, c):
    return (c == b[81] and c == b[82] and c == b[83]) \
        or (c == b[89] and c == b[94] and (c == b[79] or c == b[99]))


def is_win85(b, c):
    return (c == b[86] and c == b[87] and c == b[88]) \
        or (c == b[80] and c == b[90] and (c == b[75] or c == b[95]))


def is_win86(b, c):
    return (c == b[87] and c == b[88] and (c == b[85] or c == b[89])) \
        or (c == b[81] and c == b[91] and (c == b[76] or c == b[96]))


def is_win87(b, c):
    return (c == b[86] and c == b[88] and (c == b[85] or c == b[89])) \
        or (c == b[82] and c == b[92] and (c == b[77] or c == b[97])) \
        or (c == b[81] and c == b[93] and (c == b[75] or c == b[99]))


def is_win88(b, c):
    return (c == b[86] and c == b[87] and (c == b[85] or c == b[89])) \
        or (c == b[83] and c == b[93] and (c == b[78] or c == b[98])) \
        or (c == b[36] and c == b[62] and (c == b[10] or c == b[114]))


def is_win89(b, c):
    return (c == b[86] and c == b[87] and c == b[88]) \
        or (c == b[84] and c == b[94] and (c == b[79] or c == b[99]))


def is_win90(b, c):
    return (c == b[91] and c == b[92] and c == b[93]) \
        or (c == b[80] and c == b[85] and (c == b[75] or c == b[95])) \
        or (c == b[30] and c == b[60] and (c == b[0] or c == b[120]))


def is_win91(b, c):
    return (c == b[92] and c == b[93] and (c == b[90] or c == b[94])) \
        or (c == b[81] and c == b[86] and (c == b[76] or c == b[96])) \
        or (c == b[31] and c == b[61] and (c == b[1] or c == b[121]))


def is_win92(b, c):
    return (c == b[91] and c == b[93] and (c == b[90] or c == b[94])) \
        or (c == b[82] and c == b[87] and (c == b[77] or c == b[97])) \
        or (c == b[32] and c == b[62] and (c == b[2] or c == b[122]))


def is_win93(b, c):
    return (c == b[91] and c == b[92] and (c == b[90] or c == b[94])) \
        or (c == b[83] and c == b[88] and (c == b[78] or c == b[98])) \
        or (c == b[81] and c == b[87] and (c == b[75] or c == b[99])) \
        or (c == b[41] and c == b[67] and (c == b[15] or c == b[119])) \
        or (c == b[33] and c == b[63] and (c == b[3] or c == b[123])) \
        or (c == b[31] and c == b[62] and (c == b[0] or c == b[124]))


def is_win94(b, c):
    return (c == b[91] and c == b[92] and c == b[93]) \
        or (c == b[84] and c == b[89] and (c == b[79] or c == b[99])) \
        or (c == b[34] and c == b[64] and (c == b[4] or c == b[124]))


def is_win95(b, c):
    return (c == b[96] and c == b[97] and c == b[98]) \
        or (c == b[80] and c == b[85] and c == b[90])


def is_win96(b, c):
    return (c == b[97] and c == b[98] and (c == b[95] or c == b[99])) \
        or (c == b[81] and c == b[86] and c == b[91])


def is_win97(b, c):
    return (c == b[96] and c == b[98] and (c == b[95] or c == b[99])) \
        or (c == b[82] and c == b[87] and c == b[92])


def is_win98(b, c):
    return (c == b[96] and c == b[97] and (c == b[95] or c == b[99])) \
        or (c == b[83] and c == b[88] and c == b[93]) \
        or (c == b[46] and c == b[72] and (c == b[20] or c == b[124]))


def is_win99(b, c):
    return (c == b[96] and c == b[97] and c == b[98]) \
        or (c == b[84] and c == b[89] and c == b[94]) \
        or (c == b[81] and c == b[87] and c == b[93])


def is_win100(b, c):
    return (c == b[101] and c == b[102] and c == b[103]) \
        or (c == b[105] and c == b[110] and c == b[115]) \
        or (c == b[106] and c == b[112] and c == b[118]) \
        or (c == b[25] and c == b[50] and c == b[75])


def is_win101(b, c):
    return (c == b[102] and c == b[103] and (c == b[100] or c == b[104])) \
        or (c == b[106] and c == b[111] and c == b[116]) \
        or (c == b[26] and c == b[51] and c == b[76])


def is_win102(b, c):
    return (c == b[101] and c == b[103] and (c == b[100] or c == b[104])) \
        or (c == b[107] and c == b[112] and c == b[117]) \
        or (c == b[27] and c == b[52] and c == b[77])


def is_win103(b, c):
    return (c == b[101] and c == b[102] and (c == b[100] or c == b[104])) \
        or (c == b[108] and c == b[113] and c == b[118]) \
        or (c == b[28] and c == b[53] and c == b[78])


def is_win104(b, c):
    return (c == b[101] and c == b[102] and c == b[103]) \
        or (c == b[109] and c == b[114] and c == b[119]) \
        or (c == b[26] and c == b[52] and c == b[78]) \
        or (c == b[29] and c == b[54] and c == b[79])


def is_win105(b, c):
    return (c == b[106] and c == b[107] and c == b[108]) \
        or (c == b[110] and c == b[115] and (c == b[100] or c == b[120])) \
        or (c == b[30] and c == b[55] and c == b[80])


def is_win106(b, c):
    return (c == b[107] and c == b[108] and (c == b[105] or c == b[109])) \
        or (c == b[111] and c == b[116] and (c == b[101] or c == b[121])) \
        or (c == b[112] and c == b[118] and (c == b[100] or c == b[124])) \
        or (c == b[31] and c == b[56] and c == b[81])


def is_win107(b, c):
    return (c == b[106] and c == b[108] and (c == b[105] or c == b[109])) \
        or (c == b[112] and c == b[117] and (c == b[102] or c == b[122])) \
        or (c == b[32] and c == b[57] and c == b[82])


def is_win108(b, c):
    return (c == b[106] and c == b[107] and (c == b[105] or c == b[109])) \
        or (c == b[113] and c == b[118] and (c == b[103] or c == b[123])) \
        or (c == b[33] and c == b[58] and c == b[83])


def is_win109(b, c):
    return (c == b[106] and c == b[107] and c == b[108]) \
        or (c == b[114] and c == b[119] and (c == b[104] or c == b[124])) \
        or (c == b[31] and c == b[57] and c == b[83]) \
        or (c == b[34] and c == b[59] and c == b[84])


def is_win110(b, c):
    return (c == b[111] and c == b[112] and c == b[113]) \
        or (c == b[105] and c == b[115] and (c == b[100] or c == b[120])) \
        or (c == b[35] and c == b[60] and c == b[85])


def is_win111(b, c):
    return (c == b[112] and c == b[113] and (c == b[110] or c == b[114])) \
        or (c == b[106] and c == b[116] and (c == b[101] or c == b[121])) \
        or (c == b[36] and c == b[61] and c == b[86])


def is_win112(b, c):
    return (c == b[111] and c == b[113] and (c == b[110] or c == b[114])) \
        or (c == b[107] and c == b[117] and (c == b[102] or c == b[122])) \
        or (c == b[106] and c == b[118] and (c == b[100] or c == b[124])) \
        or (c == b[37] and c == b[62] and c == b[87])


def is_win113(b, c):
    return (c == b[111] and c == b[112] and (c == b[110] or c == b[114])) \
        or (c == b[108] and c == b[118] and (c == b[103] or c == b[123])) \
        or (c == b[38] and c == b[63] and c == b[88])


def is_win114(b, c):
    return (c == b[111] and c == b[112] and c == b[113]) \
        or (c == b[109] and c == b[119] and (c == b[104] or c == b[124])) \
        or (c == b[36] and c == b[62] and c == b[88]) \
        or (c == b[39] and c == b[64] and c == b[89])


def is_win115(b, c):
    return (c == b[116] and c == b[117] and c == b[118]) \
        or (c == b[105] and c == b[110] and (c == b[100] or c == b[120])) \
        or (c == b[40] and c == b[65] and c == b[90])


def is_win116(b, c):
    return (c == b[117] and c == b[118] and (c == b[115] or c == b[119])) \
        or (c == b[106] and c == b[111] and (c == b[101] or c == b[121])) \
        or (c == b[41] and c == b[66] and c == b[91])


def is_win117(b, c):
    return (c == b[116] and c == b[118] and (c == b[115] or c == b[119])) \
        or (c == b[107] and c == b[112] and (c == b[102] or c == b[122])) \
        or (c == b[42] and c == b[67] and c == b[92])


def is_win118(b, c):
    return (c == b[116] and c == b[117] and (c == b[115] or c == b[119])) \
        or (c == b[108] and c == b[113] and (c == b[103] or c == b[123])) \
        or (c == b[106] and c == b[112] and (c == b[100] or c == b[124])) \
        or (c == b[43] and c == b[68] and c == b[93])


def is_win119(b, c):
    return (c == b[116] and c == b[117] and c == b[118]) \
        or (c == b[109] and c == b[114] and (c == b[104] or c == b[124])) \
        or (c == b[41] and c == b[67] and c == b[93]) \
        or (c == b[44] and c == b[69] and c == b[94])


def is_win120(b, c):
    return (c == b[121] and c == b[122] and c == b[123]) \
        or (c == b[105] and c == b[110] and c == b[115]) \
        or (c == b[30] and c == b[60] and c == b[90]) \
        or (c == b[45] and c == b[70] and c == b[95])


def is_win121(b, c):
    return (c == b[122] and c == b[123] and (c == b[120] or c == b[124])) \
        or (c == b[106] and c == b[111] and c == b[116]) \
        or (c == b[31] and c == b[61] and c == b[91]) \
        or (c == b[46] and c == b[71] and c == b[96])


def is_win122(b, c):
    return (c == b[121] and c == b[123] and (c == b[120] or c == b[124])) \
        or (c == b[107] and c == b[112] and c == b[117]) \
        or (c == b[32] and c == b[62] and c == b[92]) \
        or (c == b[47] and c == b[72] and c == b[97])


def is_win123(b, c):
    return (c == b[121] and c == b[122] and (c == b[120] or c == b[124])) \
        or (c == b[108] and c == b[113] and c == b[118]) \
        or (c == b[33] and c == b[63] and c == b[93]) \
        or (c == b[48] and c == b[73] and c == b[98])


def is_win124(b, c):
    return (c == b[121] and c == b[122] and c == b[123]) \
        or (c == b[109] and c == b[114] and c == b[119]) \
        or (c == b[106] and c == b[112] and c == b[118]) \
        or (c == b[46] and c == b[72] and c == b[98]) \
        or (c == b[34] and c == b[64] and c == b[94]) \
        or (c == b[31] and c == b[62] and c == b[93]) \
        or (c == b[49] and c == b[74] and c == b[99])


checkmap = [
    is_win0, is_win1, is_win2, is_win3, is_win4,
    is_win5, is_win6, is_win7, is_win8, is_win9,
    is_win10, is_win11, is_win12, is_win13, is_win14,
    is_win15, is_win16, is_win17, is_win18, is_win19,
    is_win20, is_win21, is_win22, is_win23, is_win24,
    is_win25, is_win26, is_win27, is_win28, is_win29,
    is_win30, is_win31, is_win32, is_win33, is_win34,
    is_win35, is_win36, is_win37, is_win38, is_win39,
    is_win40, is_win41, is_win42, is_win43, is_win44,
    is_win45, is_win46, is_win47, is_win48, is_win49,
    is_win50, is_win51, is_win52, is_win53, is_win54,
    is_win55, is_win56, is_win57, is_win58, is_win59,
    is_win60, is_win61, is_win62, is_win63, is_win64,
    is_win65, is_win66, is_win67, is_win68, is_win69,
    is_win70, is_win71, is_win72, is_win73, is_win74,
    is_win75, is_win76, is_win77, is_win78, is_win79,
    is_win80, is_win81, is_win82, is_win83, is_win84,
    is_win85, is_win86, is_win87, is_win88, is_win89,
    is_win90, is_win91, is_win92, is_win93, is_win94,
    is_win95, is_win96, is_win97, is_win98, is_win99,
    is_win100, is_win101, is_win102, is_win103, is_win104,
    is_win105, is_win106, is_win107, is_win108, is_win109,
    is_win110, is_win111, is_win112, is_win113, is_win114,
    is_win115, is_win116, is_win117, is_win118, is_win119,
    is_win120, is_win121, is_win122, is_win123, is_win124,
]
