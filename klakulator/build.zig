const std = @import("std");

//Kind of a joke, but it works
//di zig gaada goto co wtf

fn leftmostloc(a: i32) i32 {
    const edge: u32 = 1 << 31;
    var roam: u32 = @bitCast(u32, a);

    if (edge & roam != 0) return 0;
    roam = roam << 1;
    if (edge & roam != 0) return 1;
    roam = roam << 1;
    if (edge & roam != 0) return 2;
    roam = roam << 1;
    if (edge & roam != 0) return 3;
    roam = roam << 1;
    if (edge & roam != 0) return 4;
    roam = roam << 1;
    if (edge & roam != 0) return 5;
    roam = roam << 1;
    if (edge & roam != 0) return 6;
    roam = roam << 1;
    if (edge & roam != 0) return 7;
    roam = roam << 1;
    if (edge & roam != 0) return 8;
    roam = roam << 1;
    if (edge & roam != 0) return 9;
    roam = roam << 1;
    if (edge & roam != 0) return 10;
    roam = roam << 1;
    if (edge & roam != 0) return 11;
    roam = roam << 1;
    if (edge & roam != 0) return 12;
    roam = roam << 1;
    if (edge & roam != 0) return 13;
    roam = roam << 1;
    if (edge & roam != 0) return 14;
    roam = roam << 1;
    if (edge & roam != 0) return 15;
    roam = roam << 1;
    if (edge & roam != 0) return 16;
    roam = roam << 1;
    if (edge & roam != 0) return 17;
    roam = roam << 1;
    if (edge & roam != 0) return 18;
    roam = roam << 1;
    if (edge & roam != 0) return 19;
    roam = roam << 1;
    if (edge & roam != 0) return 20;
    roam = roam << 1;
    if (edge & roam != 0) return 21;
    roam = roam << 1;
    if (edge & roam != 0) return 22;
    roam = roam << 1;
    if (edge & roam != 0) return 23;
    roam = roam << 1;
    if (edge & roam != 0) return 24;
    roam = roam << 1;
    if (edge & roam != 0) return 25;
    roam = roam << 1;
    if (edge & roam != 0) return 26;
    roam = roam << 1;
    if (edge & roam != 0) return 27;
    roam = roam << 1;
    if (edge & roam != 0) return 28;
    roam = roam << 1;
    if (edge & roam != 0) return 29;
    roam = roam << 1;
    if (edge & roam != 0) return 30;
    return 31;
}

fn add(a: i32, b: i32) i32 {
    var carry: i32 = 0;
    var noncarry: i32 = 0;
    var temp: i32 = 0;

    carry = a & b;
    noncarry = a ^ b;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    if (carry == 0) return noncarry;
    carry = carry << 1;
    temp = noncarry;
    noncarry = noncarry ^ carry;
    carry = temp & carry;

    return noncarry;
}

fn subtr(a: i32, b: i32) i32 {
    return add(add(a, ~b), 1);
}

fn mult(a: i32, b: i32) i32 {
    var x: i32 = a;
    var y: i32 = b;
    var result: i32 = 0;
    var negative: bool = false;

    if (x < 0) {
        x = ~x;
        x = add(x, 1);
        negative = !negative;
    }
    if (y < 0) {
        y = ~y;
        y = add(y, 1);
        negative = !negative;
    }

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    if (y == 0) {
        if (negative) {
            return add(~result, 1);
        } else {
            return result;
        }
    }
    if (y & 1 == 1) result += x;
    x = x << 1;
    y = y >> 1;

    return result;
}

fn div(a: i32, b: i32) i32 {
    var x: i32 = a;
    var y: i32 = b;
    var result: i32 = 0;
    var negative: bool = false;
    var limit: i32 = leftmostloc(b);

    if (x < 0) {
        x = ~x;
        x = add(x, 1);
        negative = !negative;
    }
    if (y < 0) {
        y = ~y;
        y = add(y, 1);
        negative = !negative;
    }

    // if (y << 31 <= x) {
    //     x = subtr(x, y << 31);
    //     result = add(result, 1 << 31);
    // }

    if (y << 30 <= x and limit > 30) {
        x = subtr(x, y << 30);
        result = add(result, 1 << 30);
    }

    if (y << 29 <= x and limit > 29) {
        x = subtr(x, y << 29);
        result = add(result, 1 << 29);
    }

    if (y << 28 <= x and limit > 28) {
        x = subtr(x, y << 28);
        result = add(result, 1 << 28);
    }

    if (y << 27 <= x and limit > 27) {
        x = subtr(x, y << 27);
        result = add(result, 1 << 27);
    }

    if (y << 26 <= x and limit > 26) {
        x = subtr(x, y << 26);
        result = add(result, 1 << 26);
    }

    if (y << 25 <= x and limit > 25) {
        x = subtr(x, y << 25);
        result = add(result, 1 << 25);
    }

    if (y << 24 <= x and limit > 24) {
        x = subtr(x, y << 24);
        result = add(result, 1 << 24);
    }

    if (y << 23 <= x and limit > 23) {
        x = subtr(x, y << 23);
        result = add(result, 1 << 23);
    }

    if (y << 22 <= x and limit > 22) {
        x = subtr(x, y << 22);
        result = add(result, 1 << 22);
    }

    if (y << 21 <= x and limit > 21) {
        x = subtr(x, y << 21);
        result = add(result, 1 << 21);
    }

    if (y << 20 <= x and limit > 20) {
        x = subtr(x, y << 20);
        result = add(result, 1 << 20);
    }

    if (y << 19 <= x and limit > 19) {
        x = subtr(x, y << 19);
        result = add(result, 1 << 19);
    }

    if (y << 18 <= x and limit > 18) {
        x = subtr(x, y << 18);
        result = add(result, 1 << 18);
    }

    if (y << 17 <= x and limit > 17) {
        x = subtr(x, y << 17);
        result = add(result, 1 << 17);
    }

    if (y << 16 <= x and limit > 16) {
        x = subtr(x, y << 16);
        result = add(result, 1 << 16);
    }

    if (y << 15 <= x and limit > 15) {
        x = subtr(x, y << 15);
        result = add(result, 1 << 15);
    }

    if (y << 14 <= x and limit > 14) {
        x = subtr(x, y << 14);
        result = add(result, 1 << 14);
    }

    if (y << 13 <= x and limit > 13) {
        x = subtr(x, y << 13);
        result = add(result, 1 << 13);
    }

    if (y << 12 <= x and limit > 12) {
        x = subtr(x, y << 12);
        result = add(result, 1 << 12);
    }

    if (y << 11 <= x and limit > 11) {
        x = subtr(x, y << 11);
        result = add(result, 1 << 11);
    }

    if (y << 10 <= x and limit > 10) {
        x = subtr(x, y << 10);
        result = add(result, 1 << 10);
    }

    if (y << 9 <= x and limit > 9) {
        x = subtr(x, y << 9);
        result = add(result, 1 << 9);
    }

    if (y << 8 <= x and limit > 8) {
        x = subtr(x, y << 8);
        result = add(result, 1 << 8);
    }

    if (y << 7 <= x and limit > 7) {
        x = subtr(x, y << 7);
        result = add(result, 1 << 7);
    }

    if (y << 6 <= x and limit > 6) {
        x = subtr(x, y << 6);
        result = add(result, 1 << 6);
    }

    if (y << 5 <= x and limit > 5) {
        x = subtr(x, y << 5);
        result = add(result, 1 << 5);
    }

    if (y << 4 <= x and limit > 4) {
        x = subtr(x, y << 4);
        result = add(result, 1 << 4);
    }

    if (y << 3 <= x and limit > 3) {
        x = subtr(x, y << 3);
        result = add(result, 1 << 3);
    }

    if (y << 2 <= x and limit > 2) {
        x = subtr(x, y << 2);
        result = add(result, 1 << 2);
    }

    if (y << 1 <= x and limit > 1) {
        x = subtr(x, y << 1);
        result = add(result, 1 << 1);
    }

    if (y <= x and limit > 0) {
        x = subtr(x, y);
        result = add(result, 1);
    }

    if (negative) {
        return add(~result, 1);
    } else {
        return result;
    }
}

pub fn main() void {
    var num1: i32 = 1024;
    var num2: i32 = 10;
    std.debug.print("Hello, {s}!\n", .{"World"});

    var result: i32 = add(num1, num2);
    std.debug.print("Addition is: {d}\n", .{result});

    result = subtr(num1, num2);
    std.debug.print("Decrement is: {d}\n", .{result});

    result = mult(num1, num2);
    std.debug.print("Multiplication is: {d}\n", .{result});

    result = div(num1, num2);
    std.debug.print("Division is: {d}\n", .{result});
}
