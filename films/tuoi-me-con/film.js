import * as W from './engine/wb.js';
import { enrichVietnamese } from './vn_font.js';

export async function build() {
  await W.loadFont('tech', 'fonts/EMSTech.json');
  enrichVietnamese(W.FONTS['tech']);

  const tl = new W.Timeline();
  const K = new W.Pen('k', W.INK.black);
  const B = new W.Pen('b', W.INK.blue);
  const R = new W.Pen('r', W.INK.red);
  const G = new W.Pen('g', W.INK.green);

  // ─────────────────────────────────────────────────────────────
  // ZONE 1: TOP-LEFT (x: 500 - 1400, y: 180 - 750) — Đề bài & Hiện nay
  // ─────────────────────────────────────────────────────────────
  let t = 0.5;
  t = tl.draw(K, W.text('BÀI TOÁN TUỔI MẸ CON', 950, 200, { h: 72, align: 'center' }), t, { by: 2.8 });
  t = tl.draw(B, W.line(580, 250, 1320, 250, { w: 7 }), t, { by: 3.3 });

  // Hình que minh họa
  t = tl.draw(K, [
    W.circle(700, 390, 30, { w: 6 }),
    W.line(700, 420, 700, 510, { w: 6 }),
    W.line(670, 450, 730, 450, { w: 6 }),
    W.line(700, 510, 675, 570, { w: 6 }),
    W.line(700, 510, 725, 570, { w: 6 })
  ], t, { by: 4.5 });
  t = tl.draw(B, W.text('Con', 700, 630, { h: 42, align: 'center' }), t, { by: 5.0 });

  t = tl.draw(K, [
    W.circle(880, 360, 40, { w: 6 }),
    W.line(880, 400, 880, 520, { w: 6 }),
    W.poly([[880, 430], [820, 560], [940, 560], [880, 430]], { w: 5 }),
    W.line(850, 560, 850, 610, { w: 6 }),
    W.line(910, 560, 910, 610, { w: 6 })
  ], t, { by: 5.8 });
  t = tl.draw(B, W.text('Mẹ', 880, 665, { h: 42, align: 'center' }), t, { by: 6.2 });

  t = tl.draw(K, [
    W.text('Hiện nay:', 1040, 440, { h: 54 }),
    W.text('Tổng tuổi = 42', 1040, 515, { h: 62, color: W.INK.blue }),
    W.text('(Mẹ + Con = 42 tuổi)', 1040, 580, { h: 42 })
  ], t, { by: 7.2 });

  // ─────────────────────────────────────────────────────────────
  // ZONE 2: TOP-RIGHT (x: 2300 - 3500, y: 180 - 750) — Bước ngoặt 5 năm sau
  // ─────────────────────────────────────────────────────────────
  t = Math.max(t, 7.6);
  t = tl.draw(R, W.arrow(1450, 480, 2250, 480, { w: 8 }), t, { by: 8.3 });
  t = tl.draw(R, W.text('Sau 5 năm nữa...', 2450, 280, { h: 64 }), t, { by: 9.5 });
  t = tl.draw(K, [
    W.text('- Con tăng: + 5 tuổi', 2480, 370, { h: 46 }),
    W.text('- Mẹ tăng:  + 5 tuổi', 2480, 430, { h: 46 })
  ], t, { by: 11.0 });
  t = tl.draw(R, W.text('→ Cả hai mẹ con cùng tăng!', 2480, 500, { h: 48 }), t, { by: 12.0 });
  t = tl.draw(B, W.text('Tổng tuổi tăng: 5 + 5 = 10 (tuổi)', 2480, 570, { h: 50 }), t, { by: 13.0 });
  t = tl.draw(R, [
    W.text('TỔNG MỚI: 42 + 10 = 52 TUỔI', 2480, 650, { h: 56 }),
    W.rect(2450, 600, 780, 80, { w: 6, over: 8 })
  ], t, { by: 14.2 });

  // ─────────────────────────────────────────────────────────────
  // ZONE 3: BOTTOM-RIGHT (x: 2200 - 3500, y: 1100 - 1850) — Sơ đồ đoạn thẳng
  // ─────────────────────────────────────────────────────────────
  t = Math.max(t, 14.6);
  t = tl.draw(K, [
    W.text('SƠ ĐỒ ĐOẠN THẲNG (Sau 5 năm):', 2300, 1140, { h: 56 }),
    W.text('Tuổi mẹ gấp 3 lần tuổi con', 2300, 1200, { h: 44 })
  ], t, { by: 16.5 });

  const partW = 160, startX = 2480;
  t = tl.draw(K, W.text('Con:', 2300, 1290, { h: 50 }), t, { by: 17.2 });
  t = tl.draw(B, [
    W.rect(startX, 1250, partW, 45, { w: 6 }),
    W.text('1 phần', startX + 30, 1330, { h: 36 })
  ], t, { by: 18.2 });

  t = tl.draw(K, W.text('Mẹ :', 2300, 1410, { h: 50 }), t, { by: 18.8 });
  t = tl.draw(B, [
    W.rect(startX, 1370, partW, 45, { w: 6 }),
    W.rect(startX + partW, 1370, partW, 45, { w: 6 }),
    W.rect(startX + partW * 2, 1370, partW, 45, { w: 6 }),
    W.text('3 phần bằng nhau', startX + 110, 1450, { h: 36 })
  ], t, { by: 20.5 });

  const bracketX = startX + partW * 3 + 30;
  t = tl.draw(R, [
    W.line(bracketX, 1240, bracketX + 25, 1335, { w: 5 }),
    W.line(bracketX + 25, 1335, bracketX, 1430, { w: 5 }),
    W.text('} Tổng = 52 tuổi', bracketX + 35, 1355, { h: 52 })
  ], t, { by: 21.8 });

  t = tl.draw(K, W.text('- Tổng số phần: 1 + 3 = 4 (phần)', 2300, 1540, { h: 48 }), t, { by: 23.0 });
  t = tl.draw(B, W.text('- 1 phần (tuổi con sau 5 năm):', 2300, 1610, { h: 48 }), t, { by: 23.8 });
  t = tl.draw(R, [
    W.text('52 : 4 = 13 (tuổi)', 2680, 1690, { h: 60 }),
    W.circle(2900, 1670, 90, { w: 6 })
  ], t, { by: 25.2 });

  // ─────────────────────────────────────────────────────────────
  // ZONE 4: BOTTOM-LEFT (x: 450 - 1450, y: 1100 - 1850) — Hiện nay & Đáp số
  // ─────────────────────────────────────────────────────────────
  t = Math.max(t, 25.6);
  t = tl.draw(K, [
    W.text('TRỞ VỀ HIỆN NAY:', 650, 1140, { h: 58 }),
    W.line(650, 1185, 1150, 1185, { w: 6 })
  ], t, { by: 27.0 });

  t = tl.draw(K, W.text('Tuổi con hiện nay:', 650, 1260, { h: 46 }), t, { by: 27.8 });
  t = tl.draw(B, W.text('13 − 5 = 8 (tuổi)', 700, 1325, { h: 54 }), t, { by: 28.6 });

  t = tl.draw(K, W.text('Tuổi mẹ hiện nay:', 650, 1420, { h: 46 }), t, { by: 29.4 });
  t = tl.draw(B, W.text('42 − 8 = 34 (tuổi)', 700, 1485, { h: 54 }), t, { by: 30.2 });

  t = tl.draw(R, [
    W.text('ĐÁP SỐ:', 720, 1610, { h: 58 }),
    W.text('MẸ: 34 TUỔI', 680, 1690, { h: 54 }),
    W.text('CON: 8 TUỔI', 680, 1765, { h: 54 }),
    W.rect(640, 1550, 500, 250, { w: 6, over: 8 })
  ], t, { by: 32.4 });
  t = tl.draw(G, W.text('✓', 1050, 1720, { h: 75 }), t, { by: 32.8 });

  tl.end();

  const board = new W.Board(tl, {});

  // ─────────────────────────────────────────────────────────────
  // CAMERA PATH
  // ─────────────────────────────────────────────────────────────
  const cam = new W.Camera([
    // Shot 1: Đề bài & Hiện nay (t: 0s -> 7.2s)
    [0.0, 950, 480, 0.88],
    [7.0, 950, 480, 0.88],
    // Lia sang Shot 2: Bước ngoặt 5 năm sau (t: 7.2s -> 14.2s)
    [7.8, 2850, 480, 0.88],
    [14.0, 2850, 480, 0.88],
    // Lia sang Shot 3: Sơ đồ đoạn thẳng (t: 14.5s -> 25.2s)
    [14.8, 2850, 1500, 0.85],
    [24.8, 2850, 1500, 0.85],
    // Lia sang Shot 4: Hiện nay & Đáp số (t: 25.5s -> 32.5s)
    [25.8, 900, 1500, 0.88],
    [32.2, 900, 1500, 0.88],
    // Shot 5: Thu phóng toàn cảnh bảng trắng (Full board view) (t: 32.5s -> 39.0s)
    [33.0, 1900, 990, 0.45],
    [39.0, 1900, 990, 0.45]
  ]);

  board.objs.push({
    draw: (ctx, tt, c) => {
      for (const p of [K, B, R, G]) {
        W.drawMarker(ctx, p, W.penPose(p, tt, cam), c, tt);
      }
    }
  });

  // Phụ đề (Subtitles)
  const subs = [
    { t0: 0.5, t1: 7.0, text: 'Hiện nay, tổng tuổi của hai mẹ con là 42.' },
    { t0: 7.5, t1: 14.0, text: 'Sau 5 năm nữa, cả mẹ và con đều tăng 5 tuổi. Tổng mới là 52 tuổi!' },
    { t0: 14.5, t1: 20.8, text: 'Vẽ sơ đồ: Con 1 phần, mẹ 3 phần. Tổng 4 phần bằng 52 tuổi.' },
    { t0: 21.0, t1: 25.4, text: 'Giá trị 1 phần, tức tuổi con sau 5 năm, là 52 chia 4 bằng 13 tuổi.' },
    { t0: 25.8, t1: 32.0, text: 'Bớt đi 5 năm về hiện tại: Con 8 tuổi, và mẹ là 42 trừ 8 bằng 34 tuổi!' },
    { t0: 32.2, t1: 38.5, text: 'Đáp số: Mẹ 34 tuổi, Con 8 tuổi. Rất rõ ràng và trực quan!' }
  ];

  return {
    dur: 39.0,
    render: (ctx, tt) => {
      board.render(ctx, tt, cam);

      // Render burned subtitles at bottom
      for (const s of subs) {
        if (tt >= s.t0 && tt <= s.t1) {
          ctx.save();
          ctx.font = '500 36px sans-serif';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          const tw = ctx.measureText(s.text).width;
          const px = 1920 / 2;
          const py = 1080 - 70;
          // Subtitle capsule background
          ctx.fillStyle = 'rgba(255, 255, 255, 0.92)';
          ctx.beginPath();
          ctx.roundRect(px - tw / 2 - 25, py - 26, tw + 50, 52, 26);
          ctx.fill();
          ctx.strokeStyle = 'rgba(0, 0, 0, 0.15)';
          ctx.lineWidth = 1.5;
          ctx.stroke();

          // Subtitle text
          ctx.fillStyle = '#1e2229';
          ctx.fillText(s.text, px, py);
          ctx.restore();
          break;
        }
      }
    },
    ev: tl.ev,
    subs: subs,
    cues: {}
  };
}
