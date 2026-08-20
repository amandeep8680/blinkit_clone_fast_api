# Order Status & Payment Status --- Swagger Testing Guide

## 1. Order Status Values

Allowed order statuses:

``` text
placed
confirmed
packing
out-for-delivery
delivered
cancelled
```

Normal order flow:

``` text
placed
  ↓
confirmed
  ↓
packing
  ↓
out-for-delivery
  ↓
delivered
```

`cancelled` is also allowed from supported stages according to the
backend transition rules.

------------------------------------------------------------------------

## 2. Update Order Status API

Swagger may initially show:

``` json
{
  "status": "string",
  "note": "string"
}
```

Do **not** send `"string"`.

### When current status is `placed`

``` json
{
  "status": "confirmed",
  "note": "Order confirmed by manager."
}
```

### When current status is `confirmed`

``` json
{
  "status": "packing",
  "note": "Order is being packed."
}
```

### When current status is `packing`

``` json
{
  "status": "out-for-delivery",
  "note": "Order is out for delivery."
}
```

### When current status is `out-for-delivery`

``` json
{
  "status": "delivered",
  "note": "Order delivered successfully."
}
```

### Cancel Order

Where cancellation is allowed:

``` json
{
  "status": "cancelled",
  "note": "Order cancelled by manager."
}
```

------------------------------------------------------------------------

## 3. Important Order Transition Rule

The backend validates the next allowed status.

For example, this is **not allowed**:

``` text
placed → delivered
```

You should normally follow:

``` text
placed
→ confirmed
→ packing
→ out-for-delivery
→ delivered
```

The configured transitions are:

``` text
placed
→ confirmed
→ cancelled

confirmed
→ packing
→ cancelled

packing
→ out-for-delivery
→ cancelled

out-for-delivery
→ delivered
```

Once the order is `cancelled` or `delivered`, the current service does
not allow another normal status update.

------------------------------------------------------------------------

## 4. What is `note`?

`note` is not an order status.

It is a human-readable description saved with the order history.

Examples:

``` text
Order confirmed by manager.
Order is being packed.
Order dispatched for delivery.
Order delivered successfully.
Order cancelled by manager.
```

Example:

``` json
{
  "status": "packing",
  "note": "Order is being packed."
}
```

Here:

``` text
status = actual system status
note   = explanation/history message
```

------------------------------------------------------------------------

# Payment Status

## 5. Allowed Payment Status Values

Allowed values are:

``` text
pending
paid
failed
refunded
```

Swagger may show:

``` json
{
  "payment_status": "string"
}
```

Again, do **not** send `"string"`.

------------------------------------------------------------------------

## 6. Payment Pending

``` json
{
  "payment_status": "pending"
}
```

Meaning:

``` text
Payment has not completed yet.
```

------------------------------------------------------------------------

## 7. Payment Successful

``` json
{
  "payment_status": "paid"
}
```

Meaning:

``` text
Payment completed successfully.
```

------------------------------------------------------------------------

## 8. Payment Failed

``` json
{
  "payment_status": "failed"
}
```

Meaning:

``` text
Payment attempt failed.
```

------------------------------------------------------------------------

## 9. Payment Refunded

``` json
{
  "payment_status": "refunded"
}
```

Meaning:

``` text
Payment was returned/refunded.
```

------------------------------------------------------------------------

# Complete Example Testing Flow

When an order is created, the current backend initializes it as:

``` text
order status   = placed
payment status = pending
```

Then order status can be tested step-by-step.

### Step 1 --- Confirm

``` json
{
  "status": "confirmed",
  "note": "Order confirmed."
}
```

### Step 2 --- Packing

``` json
{
  "status": "packing",
  "note": "Order is being packed."
}
```

### Step 3 --- Out for Delivery

``` json
{
  "status": "out-for-delivery",
  "note": "Order dispatched."
}
```

### Step 4 --- Delivered

``` json
{
  "status": "delivered",
  "note": "Order delivered."
}
```

Payment can be updated separately. For a successful payment:

``` json
{
  "payment_status": "paid"
}
```

------------------------------------------------------------------------

## Quick Reference

  -----------------------------------------------------------------------
  Field                               Allowed Values
  ----------------------------------- -----------------------------------
  `status`                            `placed`, `confirmed`, `packing`,
                                      `out-for-delivery`, `delivered`,
                                      `cancelled`

  `payment_status`                    `pending`, `paid`, `failed`,
                                      `refunded`

  `note`                              Human-readable order history
                                      message
  -----------------------------------------------------------------------

### Remember

``` text
status         = Order kaha tak pahuncha?
payment_status = Payment ka kya hua?
note           = Status change ke baare me readable message
```
