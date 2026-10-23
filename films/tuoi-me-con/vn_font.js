// Vietnamese diacritic stroke generator for EMS single-line font
export function enrichVietnamese(G) {
  const map = {
    // lowercase accents
    'á': { b: 'a', d: ['sac'] }, 'à': { b: 'a', d: ['huyen'] }, 'ả': { b: 'a', d: ['hoi'] }, 'ã': { b: 'a', d: ['nga'] }, 'ạ': { b: 'a', d: ['nang'] },
    'â': { b: 'a', d: ['non'] }, 'ấ': { b: 'a', d: ['non_sac'] }, 'ầ': { b: 'a', d: ['non_huyen'] }, 'ẩ': { b: 'a', d: ['non_hoi'] }, 'ẫ': { b: 'a', d: ['non_nga'] }, 'ậ': { b: 'a', d: ['non_nang'] },
    'ă': { b: 'a', d: ['trang'] }, 'ắ': { b: 'a', d: ['trang_sac'] }, 'ằ': { b: 'a', d: ['trang_huyen'] }, 'ẳ': { b: 'a', d: ['trang_hoi'] }, 'ẵ': { b: 'a', d: ['trang_nga'] }, 'ặ': { b: 'a', d: ['trang_nang'] },
    'é': { b: 'e', d: ['sac'] }, 'è': { b: 'e', d: ['huyen'] }, 'ẻ': { b: 'e', d: ['hoi'] }, 'ẽ': { b: 'e', d: ['nga'] }, 'ẹ': { b: 'e', d: ['nang'] },
    'ê': { b: 'e', d: ['non'] }, 'ế': { b: 'e', d: ['non_sac'] }, 'ề': { b: 'e', d: ['non_huyen'] }, 'ể': { b: 'e', d: ['non_hoi'] }, 'ễ': { b: 'e', d: ['non_nga'] }, 'ệ': { b: 'e', d: ['non_nang'] },
    'í': { b: 'i', d: ['sac'] }, 'ì': { b: 'i', d: ['huyen'] }, 'ỉ': { b: 'i', d: ['hoi'] }, 'ĩ': { b: 'i', d: ['nga'] }, 'ị': { b: 'i', d: ['nang'] },
    'ó': { b: 'o', d: ['sac'] }, 'ò': { b: 'o', d: ['huyen'] }, 'ỏ': { b: 'o', d: ['hoi'] }, 'õ': { b: 'o', d: ['nga'] }, 'ọ': { b: 'o', d: ['nang'] },
    'ô': { b: 'o', d: ['non'] }, 'ố': { b: 'o', d: ['non_sac'] }, 'ồ': { b: 'o', d: ['non_huyen'] }, 'ổ': { b: 'o', d: ['non_hoi'] }, 'ỗ': { b: 'o', d: ['non_nga'] }, 'ộ': { b: 'o', d: ['non_nang'] },
    'ơ': { b: 'o', d: ['sung'] }, 'ớ': { b: 'o', d: ['sung_sac'] }, 'ờ': { b: 'o', d: ['sung_huyen'] }, 'ở': { b: 'o', d: ['sung_hoi'] }, 'ỡ': { b: 'o', d: ['sung_nga'] }, 'ợ': { b: 'o', d: ['sung_nang'] },
    'ú': { b: 'u', d: ['sac'] }, 'ù': { b: 'u', d: ['huyen'] }, 'ủ': { b: 'u', d: ['hoi'] }, 'ũ': { b: 'u', d: ['nga'] }, 'ụ': { b: 'u', d: ['nang'] },
    'ư': { b: 'u', d: ['sung'] }, 'ứ': { b: 'u', d: ['sung_sac'] }, 'ừ': { b: 'u', d: ['sung_huyen'] }, 'ử': { b: 'u', d: ['sung_hoi'] }, 'ữ': { b: 'u', d: ['sung_nga'] }, 'ự': { b: 'u', d: ['sung_nang'] },
    'ý': { b: 'y', d: ['sac'] }, 'ỳ': { b: 'y', d: ['huyen'] }, 'ỷ': { b: 'y', d: ['hoi'] }, 'ỹ': { b: 'y', d: ['nga'] }, 'ỵ': { b: 'y', d: ['nang'] },
    'đ': { b: 'd', d: ['bar_d'] },

    // UPPERCASE accents
    'Á': { b: 'A', d: ['sac_cap'] }, 'À': { b: 'A', d: ['huyen_cap'] }, 'Ả': { b: 'A', d: ['hoi_cap'] }, 'Ã': { b: 'A', d: ['nga_cap'] }, 'Ạ': { b: 'A', d: ['nang'] },
    'Â': { b: 'A', d: ['non_cap'] }, 'Ấ': { b: 'A', d: ['non_sac_cap'] }, 'Ầ': { b: 'A', d: ['non_huyen_cap'] }, 'Ậ': { b: 'A', d: ['non_nang_cap'] },
    'Ă': { b: 'A', d: ['trang_cap'] }, 'Ắ': { b: 'A', d: ['trang_sac_cap'] }, 'Ằ': { b: 'A', d: ['trang_huyen_cap'] }, 'Ẳ': { b: 'A', d: ['trang_hoi_cap'] }, 'Ẵ': { b: 'A', d: ['trang_nga_cap'] }, 'Ặ': { b: 'A', d: ['trang_nang_cap'] },
    'É': { b: 'E', d: ['sac_cap'] }, 'È': { b: 'E', d: ['huyen_cap'] }, 'Ẻ': { b: 'E', d: ['hoi_cap'] }, 'Ẽ': { b: 'E', d: ['nga_cap'] }, 'Ẹ': { b: 'E', d: ['nang'] },
    'Ê': { b: 'E', d: ['non_cap'] }, 'Ế': { b: 'E', d: ['non_sac_cap'] }, 'Ề': { b: 'E', d: ['non_huyen_cap'] }, 'Ệ': { b: 'E', d: ['non_nang_cap'] },
    'Í': { b: 'I', d: ['sac_cap'] }, 'Ì': { b: 'I', d: ['huyen_cap'] }, 'Ị': { b: 'I', d: ['nang'] },
    'Ó': { b: 'O', d: ['sac_cap'] }, 'Ò': { b: 'O', d: ['huyen_cap'] }, 'Ỏ': { b: 'O', d: ['hoi_cap'] }, 'Õ': { b: 'O', d: ['nga_cap'] }, 'Ọ': { b: 'O', d: ['nang'] },
    'Ô': { b: 'O', d: ['non_cap'] }, 'Ố': { b: 'O', d: ['non_sac_cap'] }, 'Ồ': { b: 'O', d: ['non_huyen_cap'] }, 'Ổ': { b: 'O', d: ['non_hoi_cap'] }, 'Ộ': { b: 'O', d: ['non_nang_cap'] },
    'Ơ': { b: 'O', d: ['sung_cap'] }, 'Ớ': { b: 'O', d: ['sung_sac_cap'] }, 'Ờ': { b: 'O', d: ['sung_huyen_cap'] }, 'Ở': { b: 'O', d: ['sung_hoi_cap'] }, 'Ỡ': { b: 'O', d: ['sung_nga_cap'] }, 'Ợ': { b: 'O', d: ['sung_nang_cap'] },
    'Ú': { b: 'U', d: ['sac_cap'] }, 'Ù': { b: 'U', d: ['huyen_cap'] }, 'Ủ': { b: 'U', d: ['hoi_cap'] }, 'Ụ': { b: 'U', d: ['nang'] },
    'Ư': { b: 'U', d: ['sung_cap'] }, 'Ứ': { b: 'U', d: ['sung_sac_cap'] }, 'Ừ': { b: 'U', d: ['sung_huyen_cap'] }, 'Ử': { b: 'U', d: ['sung_hoi_cap'] }, 'Ữ': { b: 'U', d: ['sung_nga_cap'] }, 'Ự': { b: 'U', d: ['sung_nang_cap'] },
    'Ý': { b: 'Y', d: ['sac_cap'] }, 'Ỳ': { b: 'Y', d: ['huyen_cap'] }, 'Ỵ': { b: 'Y', d: ['nang'] },
    'Đ': { b: 'D', d: ['bar_D'] },
  };

  function getStrokes(cx, top, types) {
    const res = [];
    for (const t of types) {
      if (t === 'sac') res.push([cx - 20, top + 40, cx + 50, top + 130]);
      else if (t === 'huyen') res.push([cx + 20, top + 130, cx - 50, top + 40]);
      else if (t === 'hoi') res.push([cx - 30, top + 100, cx, top + 130, cx + 30, top + 100, cx, top + 50]);
      else if (t === 'nga') res.push([cx - 45, top + 70, cx - 15, top + 115, cx + 15, top + 65, cx + 45, top + 110]);
      else if (t === 'nang') res.push([cx - 10, -50, cx + 10, -50]);
      else if (t === 'non') res.push([cx - 65, top + 45, cx, top + 125, cx + 65, top + 45]);
      else if (t === 'non_sac') { res.push([cx - 65, top + 45, cx, top + 125, cx + 65, top + 45]); res.push([cx + 35, top + 120, cx + 80, top + 190]); }
      else if (t === 'non_huyen') { res.push([cx - 65, top + 45, cx, top + 125, cx + 65, top + 45]); res.push([cx - 10, top + 190, cx - 55, top + 120]); }
      else if (t === 'non_hoi') { res.push([cx - 65, top + 45, cx, top + 125, cx + 65, top + 45]); res.push([cx + 10, top + 170, cx + 35, top + 195, cx + 60, top + 170, cx + 35, top + 130]); }
      else if (t === 'non_nga') { res.push([cx - 65, top + 45, cx, top + 125, cx + 65, top + 45]); res.push([cx + 10, top + 145, cx + 35, top + 185, cx + 60, top + 140, cx + 85, top + 180]); }
      else if (t === 'non_nang') { res.push([cx - 65, top + 45, cx, top + 125, cx + 65, top + 45]); res.push([cx - 10, -50, cx + 10, -50]); }
      else if (t === 'trang') res.push([cx - 60, top + 115, cx, top + 45, cx + 60, top + 115]);
      else if (t === 'trang_sac') { res.push([cx - 60, top + 115, cx, top + 45, cx + 60, top + 115]); res.push([cx + 25, top + 120, cx + 70, top + 190]); }
      else if (t === 'trang_huyen') { res.push([cx - 60, top + 115, cx, top + 45, cx + 60, top + 115]); res.push([cx - 5, top + 190, cx - 50, top + 120]); }
      else if (t === 'trang_nang') { res.push([cx - 60, top + 115, cx, top + 45, cx + 60, top + 115]); res.push([cx - 10, -50, cx + 10, -50]); }
      else if (t === 'sung') res.push([cx + 90, top + 40, cx + 140, top + 80, cx + 150, top + 25]);
      else if (t === 'sung_sac') { res.push([cx + 90, top + 40, cx + 140, top + 80, cx + 150, top + 25]); res.push([cx - 10, top + 40, cx + 45, top + 125]); }
      else if (t === 'sung_huyen') { res.push([cx + 90, top + 40, cx + 140, top + 80, cx + 150, top + 25]); res.push([cx + 20, top + 125, cx - 35, top + 40]); }
      else if (t === 'sung_hoi') { res.push([cx + 90, top + 40, cx + 140, top + 80, cx + 150, top + 25]); res.push([cx - 20, top + 90, cx + 10, top + 120, cx + 40, top + 90, cx + 10, top + 45]); }
      else if (t === 'sung_nga') { res.push([cx + 90, top + 40, cx + 140, top + 80, cx + 150, top + 25]); res.push([cx - 30, top + 60, cx - 5, top + 105, cx + 25, top + 55, cx + 55, top + 100]); }
      else if (t === 'sung_nang') { res.push([cx + 90, top + 40, cx + 140, top + 80, cx + 150, top + 25]); res.push([cx - 10, -50, cx + 10, -50]); }
      else if (t === 'bar_d') res.push([cx + 10, 480, cx + 190, 480]);
      // Cap equivalents
      else if (t === 'sac_cap') res.push([cx - 20, top + 30, cx + 60, top + 120]);
      else if (t === 'huyen_cap') res.push([cx + 20, top + 120, cx - 60, top + 30]);
      else if (t === 'hoi_cap') res.push([cx - 35, top + 85, cx, top + 120, cx + 35, top + 85, cx, top + 40]);
      else if (t === 'nga_cap') res.push([cx - 50, top + 60, cx - 15, top + 110, cx + 15, top + 55, cx + 50, top + 105]);
      else if (t === 'non_cap') res.push([cx - 75, top + 30, cx, top + 115, cx + 75, top + 30]);
      else if (t === 'non_sac_cap') { res.push([cx - 75, top + 30, cx, top + 115, cx + 75, top + 30]); res.push([cx + 35, top + 110, cx + 85, top + 180]); }
      else if (t === 'non_huyen_cap') { res.push([cx - 75, top + 30, cx, top + 115, cx + 75, top + 30]); res.push([cx - 10, top + 180, cx - 60, top + 110]); }
      else if (t === 'non_hoi_cap') { res.push([cx - 75, top + 30, cx, top + 115, cx + 75, top + 30]); res.push([cx + 10, top + 160, cx + 40, top + 190, cx + 70, top + 160, cx + 40, top + 120]); }
      else if (t === 'non_nang_cap') { res.push([cx - 75, top + 30, cx, top + 115, cx + 75, top + 30]); res.push([cx - 10, -50, cx + 10, -50]); }
      else if (t === 'trang_cap') res.push([cx - 70, top + 105, cx, top + 30, cx + 70, top + 105]);
      else if (t === 'trang_sac_cap') { res.push([cx - 70, top + 105, cx, top + 30, cx + 70, top + 105]); res.push([cx + 30, top + 110, cx + 75, top + 180]); }
      else if (t === 'trang_huyen_cap') { res.push([cx - 70, top + 105, cx, top + 30, cx + 70, top + 105]); res.push([cx - 5, top + 180, cx - 50, top + 110]); }
      else if (t === 'trang_hoi_cap') { res.push([cx - 70, top + 105, cx, top + 30, cx + 70, top + 105]); res.push([cx + 10, top + 150, cx + 35, top + 180, cx + 60, top + 150, cx + 35, top + 115]); }
      else if (t === 'trang_nga_cap') { res.push([cx - 70, top + 105, cx, top + 30, cx + 70, top + 105]); res.push([cx + 10, top + 135, cx + 35, top + 175, cx + 60, top + 130, cx + 85, top + 170]); }
      else if (t === 'trang_nang_cap') { res.push([cx - 70, top + 105, cx, top + 30, cx + 70, top + 105]); res.push([cx - 10, -50, cx + 10, -50]); }
      else if (t === 'sung_cap') res.push([cx + 110, top + 30, cx + 165, top + 75, cx + 175, top + 15]);
      else if (t === 'sung_sac_cap') { res.push([cx + 110, top + 30, cx + 165, top + 75, cx + 175, top + 15]); res.push([cx - 10, top + 30, cx + 55, top + 120]); }
      else if (t === 'sung_huyen_cap') { res.push([cx + 110, top + 30, cx + 165, top + 75, cx + 175, top + 15]); res.push([cx + 25, top + 120, cx - 40, top + 30]); }
      else if (t === 'sung_hoi_cap') { res.push([cx + 110, top + 30, cx + 165, top + 75, cx + 175, top + 15]); res.push([cx - 20, top + 80, cx + 10, top + 115, cx + 40, top + 80, cx + 10, top + 35]); }
      else if (t === 'sung_nga_cap') { res.push([cx + 110, top + 30, cx + 165, top + 75, cx + 175, top + 15]); res.push([cx - 30, top + 55, cx - 5, top + 100, cx + 25, top + 50, cx + 55, top + 95]); }
      else if (t === 'sung_nang_cap') { res.push([cx + 110, top + 30, cx + 165, top + 75, cx + 175, top + 15]); res.push([cx - 10, -50, cx + 10, -50]); }
      else if (t === 'bar_D') res.push([cx - 160, 340, cx + 80, 340]);
    }
    return res;
  }

  for (const [ch, info] of Object.entries(map)) {
    const base = G[info.b];
    if (!base) continue;
    const w = base.w;
    const isCap = info.b === info.b.toUpperCase();
    const top = isCap ? 670 : 450;
    const cx = w * 0.5;
    const extraStrokes = getStrokes(cx, top, info.d);
    G[ch] = {
      w: w,
      s: [...base.s, ...extraStrokes]
    };
  }
}
